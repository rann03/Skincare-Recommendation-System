# Skincare Product Recommendation System

## Milestone 1

### Overview
This project aims to develop a skincare product recommendation system using machine learning. The system suggests products based on user preferences and skin characteristics.

### Report
A detailed report summarizing the work can be found [here](Milestone%201.pdf).

### Project Structure

- **data/**: Contains the dataset used for the project.
  - `cosmetics_prepared.csv`: Prepared product data.

- **deployments/**: Contains the deployment scripts and application code.
  - `app.py`: Streamlit application for user interaction.
  - `distilgpt2_recommender.py`: Script for generating recommendations using `distilgpt2`.

- **notebooks/**: Jupyter notebooks for data preparation and model experimentation. ( empty for now )

### How to Run

1. **Set Up Environment:**
   - Create and activate a virtual environment.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the App:**
   - Navigate to the `deployments` folder and run:
     ```bash
     streamlit run app.py
     ```

### References
- Hugging Face Model Hub: [DistilGPT2](https://huggingface.co/distilgpt2)
- Streamlit Documentation: [Streamlit](https://docs.streamlit.io/)