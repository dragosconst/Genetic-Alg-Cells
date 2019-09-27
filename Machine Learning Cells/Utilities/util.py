# This file will contain certain functions that are used by multiple classes or that simply couldn't fit in the 
# scope of any class
# this function checks if two objects have the same class
def areSameClass(obj1, obj2):
    return obj1.__class__.__name__ == obj2.__class__.__name__

# simpler way of getting class name of an object
def getClassName(obj):
    return obj.__class__.__name__

#check if an item is in a scene
def itemIsInScene(scene, item):
    if scene is None:
        return False
    if item is None:
        return False

    for item_ in scene.items():
        if item_ == item:
            return True

    return False