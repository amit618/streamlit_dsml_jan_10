import streamlit as st
import pickle

st.title("Car Price Prediction App")

# Define our encoding dictionary
encode_dict = {
    "fuel_type": {
        "Diesel": 1, 
        "Petrol": 2, 
        "CNG": 3, 
        "LPG": 4, 
        "Electric": 5
    },
    "transmission_type": {
        "Manual": 1, 
        "Automatic": 2
    },
    "seller_type": {
        "Dealer": 1, 
        "Individual": 2, 
        "Trustmark Dealer": 3
    }
}

model = pickle.load(open("cars24-car-price-model.pkl", "rb"))

st.subheader("Please fill in the details below:")

year = st.slider("Manufacturing Year", min_value=1990, max_value=2025, value=2018, step=1)

seller_type = st.selectbox("Seller Type", list(encode_dict["seller_type"].keys()))

km_driven = st.number_input("Kilometers Driven", min_value=0, value=40000, step=5000)

fuel_type = st.selectbox("Fuel Type", list(encode_dict["fuel_type"].keys()))

transmission_type = st.radio("Transmission Type", list(encode_dict["transmission_type"].keys()))

mileage = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0, step=0.5)

engine = st.number_input("Engine (CC)", min_value=500, max_value=5000, value=1200, step=100)

max_power = st.number_input("Max Power (bhp)", min_value=50.0, max_value=500.0, value=85.0, step=5.0)

seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10])

#['year', 'seller_type', 'km_driven', 'fuel_type', 'transmission_type', 'mileage', 'engine', 'max_power', 'seats']
def model_pred(
    year, seller_type, km_driven, fuel_type, 
    transmission_type, mileage, engine, max_power, seats
):
	# Convert categorical features using the encode dictionary
    seller_type_enc = encode_dict["seller_type"][seller_type]
    fuel_type_enc = encode_dict["fuel_type"][fuel_type]
    transmission_type_enc = encode_dict["transmission_type"][transmission_type]
    
	# standardise all the floating point data, assume mean as mu and standard deviation as std
    
	#year = (year - mu_year) / std_year
	#km_driven = (km_driven - mu_km_driven) / std_km_driven
	#mileage = (mileage - mu_mileage) / std_mileage
	#engine = (engine - mu_engine) / std_engine
	#max_power = (max_power - mu_max_power) / std_max_power
    
	# Ensure numeric features are floats or ints as needed
    data = [[
        float(year),
        seller_type_enc,
        float(km_driven),
        fuel_type_enc,
        transmission_type_enc,
        float(mileage),
        float(engine),
        float(max_power),
        float(seats)
    ]]
    

    
	# Predict
    prediction = model.predict(data)
    return round(prediction[0], 2)


if st.button("Predict"):
    price = model_pred(
        year, seller_type, km_driven, 
        fuel_type, transmission_type, 
        mileage, engine, max_power, seats
    )
    st.write(f"**Predicted Car Price**: {price} Lakhs (approx.)")
else:
    st.write("Click the **Predict** button once you've entered all the details.")