import pytest
from werkzeug.test import Client
import main


@pytest.fixture()
def app():
    app = main.app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    

    yield app


def testRequestTransection(client):
    
    response = client.get("/transaction/1")
    assert response.status_code==200

def testGetAccountDetails():
   
    response = main.get_user_details(1)
    assert response.status_code==200
   
if __name__ == "__main__":
    client=Client(app)
    
    testRequestTransection(client)
    print("Everything passed")