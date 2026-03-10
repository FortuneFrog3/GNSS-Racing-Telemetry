# ChronoBox

How to run   

1. Create virtual envioroment:     
(Windows)   
``python -m venv .venv``   

2. Activate it:  
  (Windows) 
  ``.venv\Scripts\activate `` 
  (Mac or Linux) 
  ``source .venv/bin/activate``

3. Activate it:  
(Windows)   
``.venv\Scripts\activate``   

(Mac or Linux)   
``source .venv\bin\activate``   

5. Install libraries:  
``pip install  -r requirements.txt``   

6. Run:  
``python -m src.main``   

This project uses Pytest for automated testing through Github Actions.   
Pytest is installed through Step #3, but to manually install Pytest:   
``pip install pytest``   

To manually run tests, type this in the project root:     
  ``pytest``   

This will run all tests in the tests/ folder and output a summary.
