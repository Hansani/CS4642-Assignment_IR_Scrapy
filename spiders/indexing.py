import pysolr,json,argparse

parser = argparse.ArgumentParser(description='load json into python.')
parser.add_argument('input_file', metavar='input', type=str, help='json input file')
parser.add_argument('solr_url', metavar='url', type=str, help='solr URL')

args = parser.parse_args()
solr = pysolr.Solr(args.solr_url, timeout=10)

tutorials = json.load(open(args.input_file))
for tutorial in tutorials:
  tutorial['id'] = tutorial['topic']

solr.add(tutorials)