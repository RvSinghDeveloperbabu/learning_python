# SI= Principal number + Time + Rate/100

principal = int(input("Enter the principal: "))
years = float(input("Enter the period in years: "))
rate = float(input("Enter rate of interest: "))

interest = (principal * rate * years)/100

print(f"The interest on the Principal amount: ${principal} for {years} years at the interest rate of {rate}% is ${interest}")