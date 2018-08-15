# Building APIs with Django REST Framework

Note: [code_samples.md](code_samples.md) contains code samples for the training.

## Getting set up

1. Download this repository using git clone:

    ```
    git clone https://github.com/shaunagm/building-APIs-with-DRF.git
    ```

2. Set up a virtual environment which uses Python 3.  You may need to
[install virtualenv](https://virtualenv.pypa.io/en/stable/installation/) and/or
[install Python 3](https://www.python.org/downloads/release/python-364/).
Once you've got everything installed, you can create a virtualenv with the
following command:

    ```
    virtualenv -p python3 venv
    ```

   Then, you can run the virtual environment with the command:

    ```
    source venv/bin/activate
    ```

3. Next, install the project requirements:

    ```
    pip install -r requirements.txt
    ```

4. Run the project and check that everything’s working.  Navigate to the
mysite directory and run:

    ```
    python manage.py runserver
    ```

   Then, you can open up the project in your browser.  You should see a message
   telling you that you've finished setting up.
