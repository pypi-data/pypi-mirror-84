# sql-data-api-client-Python
SQL Data Api client for Python

### Usage
```py
    """Sql Data Api"""
    SqlDataApi.set_api_url("https://localhost:44302")
    SqlDataApi.set_authentication("12121212-token-21121212")

    # query data
    result = SqlDataApi("SQL-Shared").run_query_to_array("test1.Sample100",
        filter="country = @country",
        filter_params={"country": "UK"}
    )
    print(result)

    # save data
    status = SqlDataApi("SQL-Shared").save_array("test1.Sample100", result)
    print(status)

    # execute stored procedure
    sp_res = SqlDataApi("northwind-db-connection").execute_sp_to_array("northwind.NorthwindEmployeesSummary", {'startDate': "2019-01-01", 'endDate': "2020-05-14"})
    print(sp_res)

```

### License

MIT - FalconSoft Ltd