from models.gtb_model.spool_validation import validate_gtbank_AOP_Spool
from models.gtb_model.spool_analysis import AOP_Analysis


def account_opening_analytics_instance(bankName, aopFilePath):
    """ Method to run the account opening analytics instance

    Args:
        bankName (String): The name of the supported bank [gtbank]
        aopFilePath (String): filepath to the account opening file

    Raises:
        IOError: The bank provided is not supported, please provide a supported bank

    Returns:
        tuple: fileData, errors (return value tuple should be unpacked)
    """
    if bankName == "gtbank":
        headerData, fileData, errors = validate_gtbank_AOP_Spool(
            aopFilePath=aopFilePath)

    else:
        raise IOError(
            "The bank provided is not supported, please provide a supported bank")

    return headerData, fileData, errors


aopFilePath = r"/Users/stephensanwo/Documents/Projects/automatedIAReviewMicroservice/test-data/account-opening-spools/911 Account Opened by Branch.xlsx"


try:
    headerData, fileData, errors = account_opening_analytics_instance(
        'gtbank', aopFilePath)
    # print(fileData)
    fileData.to_csv(
        r"/Users/stephensanwo/Documents/Projects/automatedIAReviewMicroservice/test-data/result.csv")
except IOError:
    fileData = ""
    errors = {"Error Description": "The Account Opening Spool provided has an invalid or unsupported extansion. Please provide the spool as is"}
    print(errors)


aop_analysis_instance = AOP_Analysis(fileData, bankName="gtbank")

accountsWoPhoneNumber, accountsWoEmail, accountsWoAddress = aop_analysis_instance.missingInfoAnalysis()

print(accountsWoPhoneNumber)
