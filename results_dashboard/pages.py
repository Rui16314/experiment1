from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import plotly.express as px
import pandas as pd
from django.db.models import Avg, Count, Q
from otree.models import Participant


class ResultsDashboard(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        # Get all participants in this session
        participants = Participant.objects.filter(session=self.session)
        
        # Prepare data for visualizations
        data = self.prepare_visualization_data(participants)
        
        return {
            'participants_data': data['participants'],
            'gender_chart': data['gender_chart'],
            'age_chart': data['age_chart'],
            'valuation_chart': data['valuation_chart'],
            'bid_chart': data['bid_chart']
        }
    
    def prepare_visualization_data(self, participants):
        # This is a simplified version - you'll need to adapt based on your actual data model
        
        # Example data structure - replace with your actual data collection
        participant_data = []
        for p in participants:
            # Get participant's custom fields if they exist
            gender = getattr(p, 'gender', 'Not specified')
            age = getattr(p, 'age', 0)
            race = getattr(p, 'race', 'Not specified')
            
            participant_data.append({
                'id': p.id,
                'gender': gender,
                'age': age,
                'race': race,
                # Add more fields as needed
            })
        
        # Create sample visualizations (replace with your actual data)
        df = pd.DataFrame(participant_data)
        
        # Gender distribution chart
        if not df.empty and 'gender' in df.columns:
            gender_counts = df['gender'].value_counts()
            gender_chart = px.bar(
                x=gender_counts.index, 
                y=gender_counts.values,
                title='Gender Distribution',
                labels={'x': 'Gender', 'y': 'Count'}
            ).to_html()
        else:
            gender_chart = "<p>No gender data available</p>"
        
        # Age distribution chart
        if not df.empty and 'age' in df.columns:
            age_chart = px.histogram(
                df, x='age', 
                title='Age Distribution',
                labels={'age': 'Age', 'count': 'Count'}
            ).to_html()
        else:
            age_chart = "<p>No age data available</p>"
        
        # Sample valuation distribution (replace with actual valuation data)
        valuation_chart = px.histogram(
            x=[50, 60, 70, 80, 90, 30, 40, 50, 60, 70], 
            title='Valuation Distribution',
            labels={'x': 'Valuation', 'y': 'Count'}
        ).to_html()
        
        # Sample bid distribution (replace with actual bid data)
        bid_chart = px.histogram(
            x=[40, 45, 50, 55, 60, 35, 40, 45, 50, 55], 
            title='Bid Distribution',
            labels={'x': 'Bid Amount', 'y': 'Count'}
        ).to_html()
        
        return {
            'participants': participant_data,
            'gender_chart': gender_chart,
            'age_chart': age_chart,
            'valuation_chart': valuation_chart,
            'bid_chart': bid_chart
        }


page_sequence = [ResultsDashboard]
