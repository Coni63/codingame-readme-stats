![code coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Coni63/6c21abaea3a4f99c473fb817ce695722/raw/covbadge.json)
![tests results](https://github.com/Coni63/codingame-readme-stats/actions/workflows/python-app.yml/badge.svg)

```
cd api
venv/Scripts/activate.ps1
python app.py
```


```
cd api
venv/Scripts/activate.ps1
coverage run -m unittest discover
coverage xml
coverage json
# coverage html
# coverage report
# python -m unittest discover
# python -m unittest
# python -m unittest test_module1 test_module2
# python -m unittest test_module.TestClass
# python -m unittest test_module.TestClass.test_method
```


```
cd api
venv/Scripts/activate.ps1
pip freeze > requirements.txt
```


```
cd api
python -m venv venv
venv/Scripts/activate.ps1
pip install -r requirements.txt
```

https://nedbatchelder.com/blog/202209/making_a_coverage_badge.html
