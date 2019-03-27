import argparse
import csv
import datetime
import os
import requests
import time


class PPP:
    PETITIONS_URL = "https://petition.parliament.uk/petitions/"

    def __init__(self, petition_number, output_dir, frequency):
        assert isinstance(petition_number, int), "Petition number must be an integer"
        self._prev_signature_count = None

        if not os.path.exists(output_dir):
            print("Creating directory {}".format(output_dir))
            os.makedirs(output_dir)
        self.output_dir = output_dir
        self._frequency = frequency
        if frequency is None:
            self._run_once(petition_number)
        else:
            self._run_multiple(petition_number)

    def _update_count(self, count):
        msg = "Current number of signatures: {}".format(count)
        if self._prev_signature_count is not None and self._frequency is not None:
            count_increase = count - self._prev_signature_count
            rate = (60/self._frequency)*count_increase
            msg += " It's increasing at a rate of {} signatures per hour.".format(rate)
        self._prev_signature_count = count
        print(msg)

    def _run_multiple(self, petition_number):
        assert self._frequency > 0, "Frequency must be a positive number"

        print("Collecting data from petition {} every {} minutes.".format(petition_number, self._frequency))
        while True:
            try:
                print("Collecting data. {}.".format(datetime.datetime.now()))
                self._run_once(petition_number)
                print("Next collecting data at {}.\n".format(datetime.datetime.now() +
                                                           datetime.timedelta(minutes=self._frequency)))
                time.sleep(60*self._frequency)
            except KeyboardInterrupt:
                print("Stopping data collection.")
                break

    def _run_once(self, petition_number):
        url = PPP.PETITIONS_URL + "{}.json".format(petition_number)
        print("Fetching data from {}...".format(url))
        r = requests.get(url)
        if r.status_code == 404:
            raise ValueError("Petition {} does not exist!".format(petition_number))
        elif r.status_code != 200:
            raise RuntimeError("Could not collect data. Status code {} from {}".format(r.status_code, url))
        else:
            print("Data collection successful!")
            self.full_json = r.json()
            self._update_count(self.full_json['data']['attributes']['signature_count'])
            country = self.full_json['data']['attributes']['signatures_by_country']
            constituency = self.full_json['data']['attributes']['signatures_by_constituency']

            self._convert_to_csv(constituency, "constituency{}.csv".format(petition_number))
            self._convert_to_csv(country, "country{}.csv".format(petition_number))

    def _convert_to_csv(self, data, name_suffix):
        """
        :param data: A list of dicts. Data to convert to a csv.
        :param name_suffix: string. Name to save csv file as (without time).
        """
        keys = data[0].keys()
        save_time = datetime.datetime.now()
        name_stem = "{}_{}_{}_{}_{}_".format(save_time.year, save_time.month,
                                             save_time.day, save_time.hour,
                                             save_time.minute)
        name = name_stem + name_suffix
        output_file = os.path.join(self.output_dir, name)
        with open(output_file, 'w') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a parliamentary petition.')
    parser.add_argument('--petition_number', type=int,
                        help='Petition number for which you would like to collect data.')
    parser.add_argument('--output_dir', type=str,
                        help='Path to directory to which you want to save the data',
                        default=os.path.join("data"))  # this assumes you are in the top level directory
    parser.add_argument('--frequency', type=int,
                        help='Number of minutes between successive requests for data. If this is not supplied'
                             ' then data is only collected once.')

    args = parser.parse_args()

    petition = PPP(args.petition_number, args.output_dir, args.frequency)
