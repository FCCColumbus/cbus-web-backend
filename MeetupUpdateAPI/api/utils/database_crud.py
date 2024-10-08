from ..models import MeetupIcalModel

def delete_single_object(Model, model_uuid):
    """deletes an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned
    """
    Model.objects.filter(pk=model_uuid).delete()
    if not Model.objects.get(uuid=model_uuid):
        print("Item deleted")
        
def delete_from_list_of_objects(Model, arr):
    """deletes items in the database from a list of objects

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (list): the list of objects to delete
    """
    for item in arr:
        Model.objects.filter(pk=item.uuid).delete()
        if Model.objects.filter(pk=item.uuid):
                print(f"{item} event was not deleted")

def get_single_object(Model, model_uuid):
    """gets an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned
    """
    if Model.objects.get(pk=model_uuid):
        return Model.objects.get(pk=model_uuid)

    if not Model.objects.get(pk=model_uuid):
        return "Item not found"