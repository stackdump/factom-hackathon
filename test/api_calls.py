from petfax import factom

# Default settings
#print(factom.info())
#print(factom.chains())
print(factom.create_chain(external_ids=['foo', 'bar'], content='hello: world'))

CHAIN = {u'entry_hash': u'f1e2899734c734c26d8b463c01dadd460947f5e2679048b27005c8a1fc27e210',
        u'chain_id': u'92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'}

#print(factom.chain_search(external_ids=['foo', 'bar']))

SEARCH_RESULT = {u'items': [{u'external_ids': [u'Zm9v', u'YmFy'],
    u'chain_id': u'92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d',
    u'links': {u'chain': u'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'}}]}

#print(factom.chain_info(u'92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'))
#print(factom.chain_entries(u'92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'))

#print(factom.chain_add_entry(
#           chain_id='92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d',
#           external_ids=['foo', 'bar'],
#           content='hello: world'
#       ))

ENTRY = {u'entry_hash': u'f1e2899734c734c26d8b463c01dadd460947f5e2679048b27005c8a1fc27e210'}

#print(factom.chain_entry_search(
#           chain_id='92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d',
#           external_ids=['foo', 'bar']
#      ))

ENTRY_SEARCH_RESULT = {u'items': [{u'external_ids': [u'Zm9v', u'YmFy'],
    u'entry_hash': u'f1e2899734c734c26d8b463c01dadd460947f5e2679048b27005c8a1fc27e210',
    u'links': {u'entry': u'https://apiplus-api-sandbox-testnet.factom.com/v1/chains/92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d/entries/f1e2899734c734c26d8b463c01dadd460947f5e2679048b27005c8a1fc27e210'}}]}

#print(factom.chain_entry_first( chain_id='92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'))
#print(factom.chain_entry_last( chain_id='92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d'))
#print(factom.chain_get_entry(
#           chain_id='92475004e70f41b94750f4a77bf7b430551113b25d3d57169eadca5692bb043d',
#           entry_hash='f1e2899734c734c26d8b463c01dadd460947f5e2679048b27005c8a1fc27e210'
#      ))
