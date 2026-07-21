"""
MODULE 3: PRODUCTION DATA QUALITY GOVERNANCE GATE
BUSINESS PURPOSE: Enforces strict structural schema data contracts at runtime.
"""
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# The structural business rulebook blueprint
DATA_CONTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "bitcoin": {
            "type": "object",
            "properties": {
                "usd": {"type": "string"}
            },
            "required": ["usd"]
        }
    },
    "required": ["bitcoin"]
}

def verify_data_contract(data_payload):
    """
    Asserts payload integrity before allowing entries to mutate database states.
    Fulfills Randstad Mandate: 'Troubleshoot incidents using custom quality frameworks'
    """
    if not data_payload:
        print("GOVERNANCE CONTROL: Payload is empty. Validation rejected.")
        return False
        
    try:
        validate(instance=data_payload, schema=DATA_CONTRACT_SCHEMA)
        print("GOVERNANCE CONTROL: Contract verified. Payload passes schema constraints.")
        return True
    except ValidationError as error:
        print(f"\nCRITICAL GOVERNANCE DETECTED: Corrupted payload blocked! Reason: {error.message}\n")
        return False
