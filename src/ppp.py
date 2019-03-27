import argparse
import csv
import os
import requests


class PPP:
    PETITIONS_URL = "https://petition.parliament.uk/petitions/"

    def __init__(self, petition_number, output_dir):
        assert isinstance(petition_number, int), "Petition number must be an integer"

        if not os.path.exists(output_dir):
            print("Creating directory {}".format(output_dir))
            os.makedirs(output_dir)
        self.output_dir = output_dir
        self._run_once(petition_number)

    def _run_once(self, petition_number):
        url = PPP.PETITIONS_URL + "{}.json".format(petition_number)
        print("Fetching data from {}...".format(url))
        r = requests.get(url)
        if r.status_code == 404:
            raise ValueError("Petition {} does not exist!".format(petition_number))
        else:
            print("Data collection successful!")
            full_json = r.json()
            country = full_json['data']['attributes']['signatures_by_country']
            constituency = full_json['data']['attributes']['signatures_by_constituency']

            self._convert_to_csv(constituency, "constituency.csv")
            self._convert_to_csv(country, "country.csv")

    def _convert_to_csv(self, data, name):
        """
        :param data: A list of dicts. Data to convert to a csv.
        :param name: string. Name to save csv file as.
        """
        keys = data[0].keys()
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

    args = parser.parse_args()

    petition = PPP(args.petition_number, args.output_dir)
