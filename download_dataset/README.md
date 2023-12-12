# Extraction from ChEMBL v33

After downloading and installing the `chembl_v33` database, extraction should be performed based on the tables `compound_properties` and `compound_structures`. You can try it out to e.g. list the first 20 records using (assuming you are logged in to the database and running mysql);

```sql
SELECT cs.canonical_smiles, cp.cx_logd
FROM compound_structures cs
JOIN compound_properties cp ON cs.molregno = cp.molregno
WHERE cs.canonical_smiles IS NOT NULL AND cp.cx_logd IS NOT NULL
LIMIT 20;
```

Extraction of all data can be performed by running this from the command line, update `[USERNAME]` and `[PASSWORD]` after your own database setup;

```bash
mysql -u [USERNAME] -p[PASSWORD] chembl_33 -e "SELECT cs.canonical_smiles, cp.cx_logd
FROM compound_structures cs
JOIN compound_properties cp ON cs.molregno = cp.molregno
WHERE cs.canonical_smiles IS NOT NULL AND cp.cx_logd IS NOT NULL" > cx_logd.csv
```

This query should be quick and the result saved in a tab-delimited CSV file `cx_logd.csv`. The compressed version of this file is saved in this directory.