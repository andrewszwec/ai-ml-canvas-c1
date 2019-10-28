import boto3
import pprint

def analyse_image_text(bucket, document):
    """ 
    Extracts text from image using AWS
    Textract and analyses text for entities
    using AWS Comprehend.
    
    Inputs:     AWS bucket name
                    string
                Document name 
                    string
    Returns:    List of detected words 
                and types in tuples.
                    list
    """

    # Setup
    client = boto3.client('textract')
    comprehend = boto3.client(service_name='comprehend')
    
    # Process image using S3 object, return text
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})
    
    # Get the text blocks
    blocks=response['Blocks']
    
    # Make a list of words
    words = [block['Text'] for block in blocks if 'Text' in block]
    text = ' '.join(words)
    
    # Get Dominant Language
    response_lang = comprehend.detect_dominant_language(Text = text)
    lang = response_lang.get('Languages')[0].get('LanguageCode') 
    
    # Get entities
    response_entities = comprehend.detect_entities(Text=text, LanguageCode=lang)
    entities = [ (entity['Text'], entity['Type']) for entity in response_entities['Entities'] ]

    return entities  
    

if __name__ == '__main__':
    bucket = '<aws_bucket_name>'
    document = '<image_name>'

    # Analyse Text
    obj = analyse_image_text(bucket, document)
    
    # Print Results
    pp = pprint.PrettyPrinter(indent=4)
    print('--------\nEntities\n--------')
    pp.pprint(obj)