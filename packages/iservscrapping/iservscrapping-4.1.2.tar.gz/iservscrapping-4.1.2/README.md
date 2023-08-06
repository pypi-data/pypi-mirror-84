# iservscrapping
This is a tool to access iserv over python.

## Get started
1. Put this module at a place where you can import it
2. Paste this code:

```python
from iservscrapping import Iserv
myiserv = Iserv("https://demo-iserv.de", "user.name", "password")
myiserv.login()

print(myiserv.get_untis_substitution_plan("/iserv/plan/show/raw/vertreter/subst_002.htm", "10a"))
print(myiserv.get_next_tests(path="/iserv"))
```

## Documentation
A full documentation for the project can be found on readthedocs: https://iservscrapping.readthedocs.io/en/latest/

## Contributing
Contributing to this project is very welcome!
By sending a PR, you agree that your code is licensed under MIT by me. You will be listed as Contributor in the Repos info.
