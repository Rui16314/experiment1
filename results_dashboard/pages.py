from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from django.db.models import Avg, Count, Q, F
from otree.models import Participant, Session
from django.apps import apps


class ResultsDashboard(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        participants = Participant.objects.filter(session=self.session)
        data = self.prepare_visualization_data(participants)
        
        return {
            'participants_data': data['participants'],
            'gender_chart': data['gender_chart'],
            'age_chart': data['age_chart'],
            'race_chart': data['race_chart'],
            'major_chart': data['major_chart'],
            'valuation_chart': data['valuation_chart'],
            'bid_chart': data['bid_chart'],
            'revenue_chart': data['revenue_chart'],
            'gender_valuation_chart': data['gender_valuation_chart'],
            'age_valuation_chart': data['age_valuation_chart'],
            'race_valuation_chart': data['race_valuation_chart'],
            'major_valuation_chart': data['major_valuation_chart']
        }
    
    def prepare_visualization_data(self, participants):
        all_bids = []
        all_valuations = []
        all_revenues = []
        all_genders = []
        all_ages = []
        all_races = []
        all_majors = []
        
        auction_apps = [
            'first_price_auction',
            'repeated_first_price_fixed', 
            'first_price_with_chat',
            'second_price_auction',
            'repeated_second_price_fixed',
            'second_price_with_chat'
        ]
        
        for app in auction_apps:
            try:
                app_models = apps.get_app_config(app).get_models()
                for model in app_models:
                    if hasattr(model, 'bid_amount') and hasattr(model, 'private_value'):
                        records = model.objects.filter(session=self.session)
                        for record in records:
                            all_bids.append(float(record.bid_amount))
                            all_valuations.append(float(record.private_value))
                            if hasattr(record, 'payoff'):
                                all_revenues.append(float(record.payoff))
            except:
                pass
        
        participant_data = []
        for p in participants:
            gender = getattr(p, 'gender', 'Not specified')
            age = getattr(p, 'age', 0)
            race = getattr(p, 'race', 'Not specified')
            major = getattr(p, 'major', 'Not specified')
            
            participant_data.append({
                'id': p.id,
                'gender': gender,
                'age': age,
                'race': race,
                'major': major
            })
            
            all_genders.append(gender)
            all_ages.append(age)
            all_races.append(race)
            all_majors.append(major)
        
        df = pd.DataFrame(participant_data)
        
        # 1. Gender distribution chart
        if not df.empty and 'gender' in df.columns:
            gender_counts = df['gender'].value_counts()
            gender_chart = px.bar(
                x=gender_counts.index, 
                y=gender_counts.values,
                title='Gender Distribution of Participants',
                labels={'x': 'Gender', 'y': 'Count'},
                color=gender_counts.index
            ).to_html()
        else:
            gender_chart = "<p>No gender data available</p>"
        
        # 2. Age distribution chart
        if not df.empty and 'age' in df.columns and any(age > 0 for age in all_ages):
            age_chart = px.histogram(
                x=all_ages, 
                title='Age Distribution of Participants',
                labels={'x': 'Age', 'y': 'Count'},
                nbins=10
            ).to_html()
        else:
            age_chart = "<p>No age data available</p>"
        
        # 3. Race distribution chart
        if not df.empty and 'race' in df.columns:
            race_counts = df['race'].value_counts()
            race_chart = px.pie(
                values=race_counts.values,
                names=race_counts.index,
                title='Race Distribution of Participants'
            ).to_html()
        else:
            race_chart = "<p>No race data available</p>"
        
        # 4. Major distribution chart
        if not df.empty and 'major' in df.columns:
            major_counts = df['major'].value_counts()
            major_chart = px.bar(
                x=major_counts.index, 
                y=major_counts.values,
                title='Major Distribution of Participants',
                labels={'x': 'Major', 'y': 'Count'}
            ).to_html()
        else:
            major_chart = "<p>No major data available</p>"
        
        # 5. Valuation distribution (grouped in intervals)
        if all_valuations:
            intervals_5 = np.arange(0, 101, 5)
            intervals_10 = np.arange(0, 101, 10)
            intervals_20 = np.arange(0, 101, 20)
            
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=('5-point Intervals', '10-point Intervals', '20-point Intervals')
            )
            
            fig.add_trace(
                go.Histogram(x=all_valuations, nbinsx=len(intervals_5)-1, name='5-point'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Histogram(x=all_valuations, nbinsx=len(intervals_10)-1, name='10-point'),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Histogram(x=all_valuations, nbinsx=len(intervals_20)-1, name='20-point'),
                row=1, col=3
            )
            
            fig.update_layout(height=400, title_text="Valuation Distribution Across Different Intervals")
            valuation_chart = fig.to_html()
        else:
            valuation_chart = "<p>No valuation data available</p>"
        
        # 6. Bid distribution
        if all_bids:
            bid_chart = px.histogram(
                x=all_bids, 
                title='Distribution of Bid Amounts',
                labels={'x': 'Bid Amount', 'y': 'Count'},
                nbins=20
            ).to_html()
        else:
            bid_chart = "<p>No bid data available</p>"
        
        # 7. Revenue comparison between auction types
        revenue_chart = "<p>Revenue comparison chart would be implemented with actual revenue data</p>"
        
        # 8. Average valuation by gender
        if not df.empty and 'gender' in df.columns and all_valuations:
            gender_valuation_chart = px.box(
                x=all_genders, y=all_valuations,
                title='Valuation Distribution by Gender',
                labels={'x': 'Gender', 'y': 'Valuation'}
            ).to_html()
        else:
            gender_valuation_chart = "<p>Insufficient data for gender-valuation analysis</p>"
        
        # 9. Average valuation by age group
        if not df.empty and any(age > 0 for age in all_ages) and all_valuations:
            age_valuation_chart = px.scatter(
                x=all_ages, y=all_valuations,
                title='Valuation by Age',
                labels={'x': 'Age', 'y': 'Valuation'},
                trendline='ols'
            ).to_html()
        else:
            age_valuation_chart = "<p>Insufficient data for age-valuation analysis</p>"
        
        # 10. Average valuation by race
        if not df.empty and 'race' in df.columns and all_valuations:
            race_valuation_chart = px.box(
                x=all_races, y=all_valuations,
                title='Valuation Distribution by Race',
                labels={'x': 'Race', 'y': 'Valuation'}
            ).to_html()
        else:
            race_valuation_chart = "<p>Insufficient data for race-valuation analysis</p>"
        
        # 11. Average valuation by major
        if not df.empty and 'major' in df.columns and all_valuations:
            major_valuation_chart = px.box(
                x=all_majors, y=all_valuations,
                title='Valuation Distribution by Major',
                labels={'x': 'Major', 'y': 'Valuation'}
            ).to_html()
        else:
            major_valuation_chart = "<p>Insufficient data for major-valuation analysis</p>"
        
        return {
            'participants': participant_data,
            'gender_chart': gender_chart,
            'age_chart': age_chart,
            'race_chart': race_chart,
            'major_chart': major_chart,
            'valuation_chart': valuation_chart,
            'bid_chart': bid_chart,
            'revenue_chart': revenue_chart,
            'gender_valuation_chart': gender_valuation_chart,
            'age_valuation_chart': age_valuation_chart,
            'race_valuation_chart': race_valuation_chart,
            'major_valuation_chart': major_valuation_chart
        }


page_sequence = [ResultsDashboard]
