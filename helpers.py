def check_response(response:dict)->dict:
    """
    Function to check that the response returned by the AI constains all the data needed.
    If all data is present return True, otherwise return False.
    """
    expense_name = response.get("expense_name",None)
    category = response.get("category",None)
    amount = response.get("amount",None)

    if expense_name and category and amount:
        return True
    return False