import pandas as pd
import streamlit as st

def calculate_future_value(principal = 1500, 
                           annual_rate = 5, 
                           times_compounded = 12, 
                           years = 35, 
                           contribution = 100, 
                           ter = 0, 
                           inflation = False):
    """
    Calculate the future value of an investment with regular contributions and compare it to a simple savings scenario.

    :param principal: Initial amount of money.
    :param annual_rate: Annual interest rate (as a percentage).
    :param times_compounded: Number of times interest is compounded per year.
    :param years: Number of years the money is invested.
    :param contribution: Regular contribution added each compounding period.
    :param ter: total expense ratio to apply to the annual rate.
    :param inflation: apply an inflation rate to the outcome.
    :return: DataFrame with the future value of the investment, contributions, and simple savings for each year.
    """
    # Prepare a list to hold data for each year
    data = []

    # Turn rates from percentage to fraction.
    annual_rate /= 100
    ter /= 100
    inflation_rate = 2 / 100 if inflation else 0
    
    # Substract TER from nominal return.
    return_after_ter = annual_rate - ter

    # Adjust annual rate for inflation: Effective return.
    # Formula Effective return = ((1 + Return after TER) / (1 + Inflation Rate)) - 1
    effective_return = ((1 + return_after_ter) / (1 + inflation_rate)) - 1 if inflation else return_after_ter

    if effective_return < 0:
        st.error("Negative returns are not allowed in this calculator! This is due to Annual Growth Rate - TER or the fact that after applying inflation, the returns go to the negative.")
        exit()

    for year in range(1, years + 1):
        if effective_return == 0:
            # With no interest, no future values.
            amount = principal 

            # Calculate future value of regular contributions
            future_value_of_contributions = contribution * (1 ** (times_compounded * year) - 1)

            # Total future value with compound interest
            future_value_with_interest = amount + future_value_of_contributions
            
            # Calculate future value if saved (no interest)
            future_value_savings = principal + contribution * times_compounded * year

            interest_over_initial_investment = amount - principal
            contributions = future_value_savings - principal
            interest_over_contributions = 0
            total_interest = interest_over_initial_investment + interest_over_contributions
        else:
            # Calculate future value of the principal
            amount = principal * (1 + effective_return / times_compounded) ** (times_compounded * year)
            
            # Calculate future value of regular contributions
            future_value_of_contributions = contribution * ((1 + effective_return / times_compounded) ** (times_compounded * year) - 1) / (effective_return / times_compounded)
            
            # Total future value with compound interest
            future_value_with_interest = amount + future_value_of_contributions

            # Calculate future value if saved (no interest)
            future_value_savings = principal + contribution * times_compounded * year
            
            interest_over_initial_investment = amount - principal
            contributions = future_value_savings - principal
            interest_over_contributions = future_value_of_contributions - contributions
            total_interest = interest_over_initial_investment + interest_over_contributions
    
        
        # Append the results to the list
        data.append({
            'Year': year,
            "Initial Investment": principal,
            "Interest over Initial Investment": interest_over_initial_investment,
            'Total Initial investment': amount,
            'Contributions': contributions,
            'Interest over Contributions': interest_over_contributions,
            'Total Contributions': future_value_of_contributions,
            "Interest": total_interest,
            'Total': 0,
        })

    # Create a DataFrame from the list
    df = pd.DataFrame(data)
    
    return df

