from django.core.exceptions import ValidationError

def file_size(Value):
    filesize = Value.size
    if filesize > 8e+9:
        raise ValidationError("Max file size is 1gb")
    


    
    