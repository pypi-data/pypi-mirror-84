from models.gtb_model.spool_validation import validate_AOP_Spool
import json

# Test Data
aopFilePath = r"/Users/stephensanwo/Documents/Projects/automatedIAReviewMicroservice/test-data/account-opening-spools/911 Account Opened by Branch.xlsx"

fileData, errors = validate_AOP_Spool(aopFilePath=aopFilePath)


# Export error logs

with open('FailedSpoolsErrorLog.json', 'w') as fp:
    json.dump(errors, fp)


print(fileData)


def wrongInfoAnalysis(self):

    # 3 - Accounts with wrong email
    def check(x):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, x)):
            return("Valid Email")
        elif x == 'No email':
            return ("No Email")
        else:
            return("Invalid Email")

    aopaccountsWoPhoneNumber = aopFileData['email validity'] = aopaccountsWoPhoneNumber = aopFileData['email'].apply(
        lambda x: check(x))
    InvalidEmails = aopaccountsWoPhoneNumber = aopFileData[aopaccountsWoPhoneNumber= aopFileData['email validity']
                                                           == 'Invalid Email'].copy()

    # 5 - Accounts opened for minors
    aopaccountsWoPhoneNumber = aopFileData[(aopaccountsWoPhoneNumber=aopFileData['Age'] > 18) & (
        aopaccountsWoPhoneNumber=aopFileData['Product Name'] == 'EARLY SAVERS')]
    MinorAccounts = aopaccountsWoPhoneNumber = aopFileData[(aopaccountsWoPhoneNumber=aopFileData['Age'] > 18) & (
        aopaccountsWoPhoneNumber=aopFileData['Product Name'] == 'EARLY SAVERS')]

    # Evergreen Issues
    Evergreen = aopaccountsWoPhoneNumber = aopFileData[(aopaccountsWoPhoneNumber=aopFileData['Age'] < 60) & (
        aopaccountsWoPhoneNumber=aopFileData['Product Name'] == 'EVERGREEN')]

    # Elderlies with large balances
    LikelyPEP = data[(data['Age'] > 60) & (
        data['Available balance'] > 1000000)]

    # Export Results

    resultsFolder = os.path.join(os.getcwd(), "Results")

    try:
        accountsWoEmail[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name', 'product code', 'email']].to_csv(
            os.path.join(resultsFolder, "Accounts opened without email address.csv"), index=False)
    except:
        PermissionError

    try:
        accountsWoAddress[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name', 'product code', 'address 1']].to_csv(
            os.path.join(resultsFolder, "Accounts opened without residential address.csv"), index=False)
    except:
        PermissionError

    try:
        InvalidEmails[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name', 'product code',
                       'phone number']].to_csv(os.path.join(resultsFolder, "Accounts opened with invalid emails.csv"), index=False)
    except:
        PermissionError

    try:
        MinorAccounts[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name',
                       'product code', 'phone number']].to_csv(os.path.join(resultsFolder, "Accounts opened for Minors.csv"), index=False)
    except:
        PermissionError

    try:
        Evergreen[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name', 'product code',
                   'phone number']].to_csv(os.path.join(resultsFolder, "Evergreen Accounts for non-elderlies.csv"), index=False)
    except:
        PermissionError

    try:
        LikelyPEP[['branch code', 'branch name', 'account number', 'customer id', 'customer', 'product name',
                   'product code', 'phone number']].to_csv(os.path.join(resultsFolder, "Likely PEP Accounts.csv"), index=False)
    except:
        PermissionError
