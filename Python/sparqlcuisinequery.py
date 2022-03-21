# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON





def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def cuisine_query(country_id):
  endpoint_url = "https://query.wikidata.org/sparql"

  query = f"""#Goats
  SELECT ?item ?itemLabel
  WHERE 
  {{
    VALUES ?food_classes {{ wd:Q177
  wd:Q6663
  wd:Q9053
  wd:Q13393
  wd:Q20734
  wd:Q28803
  wd:Q40050
  wd:Q41415
  wd:Q46383
  wd:Q81799
  wd:Q147538
  wd:Q160525
  wd:Q746549
  wd:Q182940
  wd:Q186817
  wd:Q1599125
  wd:Q191655
  wd:Q192150
  wd:Q213062
  wd:Q275068
  wd:Q322787
  wd:Q339836
  wd:Q542283
  wd:Q549980
  wd:Q667478
  wd:Q697498
  wd:Q701628
  wd:Q736427
  wd:Q832338
  wd:Q983160
  wd:Q1018075
  wd:Q1061842
  wd:Q1137679
  wd:Q1142503
  wd:Q1344218
  wd:Q1427844
  wd:Q1683302
  wd:Q1857976
  wd:Q1860324
  wd:Q1867162
  wd:Q1883153
  wd:Q1884503
  wd:Q2007824
  wd:Q2046560
  wd:Q2089470
  wd:Q2144948
  wd:Q2170924
  wd:Q2194275
  wd:Q2194659
  wd:Q2421293
  wd:Q2493720
  wd:Q2509786
  wd:Q2609925
  wd:Q2629070
  wd:Q2691193
  wd:Q2718625
  wd:Q2834371
  wd:Q2920963
  wd:Q2963582
  wd:Q2964495
  wd:Q3054617
  wd:Q3085085
  wd:Q3242685
  wd:Q3519244
  wd:Q3544584
  wd:Q3573026
  wd:Q3676249
  wd:Q4103061
  wd:Q4209872
  wd:Q4764984
  wd:Q5004791
  wd:Q5363430
  wd:Q5523588
  wd:Q5701588
  wd:Q5703544
  wd:Q5882405
  wd:Q5911091
  wd:Q6038708
  wd:Q6127173
  wd:Q6501890
  wd:Q6539361
  wd:Q2095
  wd:Q6559431
  wd:Q6941266
  wd:Q7199982
  wd:Q7230138
  wd:Q7249903
  wd:Q7339603
  wd:Q7418198
  wd:Q7813019
  wd:Q8245687
  wd:Q9392148
  wd:Q10423500
  wd:Q10514020
  wd:Q10859394
  wd:Q10859806
  wd:Q11280038
  wd:Q11559422
  wd:Q477248
  wd:Q11681782
  wd:Q14468365
  wd:Q14914664
  wd:Q15896774
  wd:Q15897086
  wd:Q16608039
  wd:Q16763507
  wd:Q17026621
  wd:Q17030355
  wd:Q17062980
  wd:Q18679149
  wd:Q18679685
  wd:Q21976260
  wd:Q23044244
  wd:Q24890754
  wd:Q24911299
  wd:Q24953260
  wd:Q25067130
  wd:Q27994917
  wd:Q27994920
  wd:Q27994921
  wd:Q27994935
  wd:Q27994938
  wd:Q28100020
  wd:Q28100665
  wd:Q28100830
  wd:Q28100865
  wd:Q28100907
  wd:Q28100912
  wd:Q28100918
  wd:Q44480854
  wd:Q44683343
  wd:Q44683918
  wd:Q56669796
  wd:Q59629576
  wd:Q60126666
  wd:Q61750516
  wd:Q64166152
  wd:Q64210788
  wd:Q64210828
  wd:Q69393237
  wd:Q84435149
  wd:Q84561722
  wd:Q84561781
  wd:Q84562176
  wd:Q84573712
  wd:Q84573718
  wd:Q84573722
  wd:Q96045946
  wd:Q97258831
  wd:Q98400272
  wd:Q99554129
  wd:Q100280511
  wd:Q100285595
  wd:Q100290176
  wd:Q100320371
  wd:Q101643769
  wd:Q105045810
  wd:Q105045833
  wd:Q105045860
  wd:Q105523063
  wd:Q105533442
  wd:Q107122728
  wd:Q108672552
  wd:Q109361903
  wd:Q109649893 }}
    ?item wdt:P495 wd:{country_id}.
    ?item wdt:P279 ?food_classes
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
  }}"""
  results = get_results(endpoint_url, query)

  dish_list = []
  for result in results["results"]["bindings"]:
    if result['itemLabel']['value'] not in dish_list:
      dish_list.append(result['itemLabel']['value'])
  print(dish_list)
  return dish_list


def fictional_universe_query(universe_id):
  
  endpoint_url = "https://query.wikidata.org/sparql"

  query = f"""#Goats
      SELECT ?item ?itemLabel 
      WHERE 
      {{
      ?item wdt:P1080 wd:{universe_id}.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
      }}"""
  results = get_results(endpoint_url, query)

  universe_list = []
  for result in results["results"]["bindings"]:
    if result['itemLabel']['value'] not in universe_list:
      universe_list.append(result['itemLabel']['value'])
  return universe_list
      
