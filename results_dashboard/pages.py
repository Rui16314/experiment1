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
        # Get all participants in this session
        participants = Participant.objects.filter(session=self.session)
        
        # Prepare data for visualizations
        data = self.prepare_visualization_data(participants)
        
        return {
            'avg_bid_behavior_chart': data['avg_bid_behavior_chart'],
            'individual_bid_behavior_charts': data['individual_bid_behavior_charts'],
            'avg_revenue_chart': data['avg_revenue_chart'],
            'avg_revenue_all_rounds': data['avg_revenue_all_rounds'],
            'all_experiments_bid_behavior': data['all_experiments_bid_behavior'],
            'all_experiments_revenue_trends': data['all_experiments_revenue_trends'],
            'all_experiments_avg_revenues': data['all_experiments_avg_revenues']
        }
    
    def prepare_visualization_data(self, participants):
        # Get all auction data from different apps
        all_bids = []
        all_valuations = []
        all_revenues = []
        all_rounds = []
        all_sessions = []
        all_participants = []
        
        # Collect data from all auction apps
        auction_apps = [
            ('first_price_auction', 'Session 1'),
            ('repeated_first_price_fixed', 'Session 2'), 
            ('first_price_with_chat', 'Session 3'),
            ('second_price_auction', 'Session 4'),
            ('repeated_second_price_fixed', 'Session 5'),
            ('second_price_with_chat', 'Session 6')
        ]
        
        for app_name, session_name in auction_apps:
            try:
                app_models = apps.get_app_config(app_name).get_models()
                for model in app_models:
                    if hasattr(model, 'bid_amount') and hasattr(model, 'private_value'):
                        records = model.objects.filter(session=self.session)
                        for record in records:
                            all_bids.append(float(record.bid_amount))
                            all_valuations.append(float(record.private_value))
                            all_rounds.append(int(getattr(record, 'round_number', 1)))
                            all_sessions.append(session_name)
                            all_participants.append(getattr(record, 'participant_id', 0))
                            
                            if hasattr(record, 'payoff') and hasattr(record, 'is_winner') and getattr(record, 'is_winner', False):
                                # For first-price auctions, revenue is the winning bid
                                if app_name in ['first_price_auction', 'repeated_first_price_fixed', 'first_price_with_chat']:
                                    all_revenues.append(float(record.bid_amount))
                                # For second-price auctions, revenue is the second highest bid
                                else:
                                    # This would need to be calculated based on group data
                                    pass
            except:
                pass
        
        # Create DataFrame for analysis
        df = pd.DataFrame({
            'bid': all_bids,
            'valuation': all_valuations,
            'round': all_rounds,
            'session': all_sessions,
            'participant_id': all_participants
        })
        
        # 1. Average bidding behavior: Horizontal axis is valuations, vertical axis is average bids
        if not df.empty:
            # Group by valuation and calculate average bid
            valuation_bins = np.arange(0, 101, 5)  # 5-point intervals
            df['valuation_bin'] = pd.cut(df['valuation'], bins=valuation_bins)
            avg_bid_by_valuation = df.groupby('valuation_bin')['bid'].mean().reset_index()
            
            avg_bid_behavior_chart = px.bar(
                avg_bid_by_valuation,
                x='valuation_bin',
                y='bid',
                title='Average Bidding Behavior by Valuation',
                labels={'valuation_bin': 'Valuation Range', 'bid': 'Average Bid'},
                color='bid'
            ).to_html()
        else:
            avg_bid_behavior_chart = "<p>No bid data available</p>"
        
        # 2. Average bidding behavior of individual students
        individual_bid_behavior_charts = []
        if not df.empty and 'participant_id' in df.columns:
            unique_participants = df['participant_id'].unique()
            for participant_id in unique_participants[:5]:  # Limit to first 5 participants for display
                participant_df = df[df['participant_id'] == participant_id]
                participant_avg_bid = participant_df.groupby('valuation_bin')['bid'].mean().reset_index()
                
                chart = px.bar(
                    participant_avg_bid,
                    x='valuation_bin',
                    y='bid',
                    title=f'Bidding Behavior - Participant {participant_id}',
                    labels={'valuation_bin': 'Valuation Range', 'bid': 'Average Bid'}
                ).to_html()
                individual_bid_behavior_charts.append(chart)
        else:
            individual_bid_behavior_charts = ["<p>No individual bid data available</p>"]
        
        # 3. Average revenue by round
        # This is a simplified version - you would need to calculate actual revenue
        if not df.empty:
            # For demonstration, using average bid as proxy for revenue
            avg_revenue_by_round = df.groupby('round')['bid'].mean().reset_index()
            
            avg_revenue_chart = px.line(
                avg_revenue_by_round,
                x='round',
                y='bid',
                title='Average Revenue by Round',
                labels={'round': 'Round Number', 'bid': 'Average Revenue'},
                markers=True
            ).to_html()
        else:
            avg_revenue_chart = "<p>No revenue data available</p>"
        
        # 4. Average revenue across all rounds
        if not df.empty:
            avg_revenue_all_rounds = df['bid'].mean()
        else:
            avg_revenue_all_rounds = 0
        
        # 5. All experiments bid behavior on same page
        if not df.empty:
            all_experiments_bid_behavior = px.box(
                df,
                x='session',
                y='bid',
                title='Bidding Behavior Across All Experiments',
                labels={'session': 'Experiment Session', 'bid': 'Bid Amount'}
            ).to_html()
        else:
            all_experiments_bid_behavior = "<p>No data available for comparison</p>"
        
        # 6. All experiments revenue trends on same page
        if not df.empty:
            revenue_by_session_round = df.groupby(['session', 'round'])['bid'].mean().reset_index()
            
            all_experiments_revenue_trends = px.line(
                revenue_by_session_round,
                x='round',
                y='bid',
                color='session',
                title='Revenue Trends Across All Experiments',
                labels={'round': 'Round Number', 'bid': 'Average Revenue', 'session': 'Experiment Session'},
                markers=True
            ).to_html()
        else:
            all_experiments_revenue_trends = "<p>No data available for comparison</p>"
        
        # 7. All experiments average revenues on same page
        if not df.empty:
            avg_revenue_by_session = df.groupby('session')['bid'].mean().reset_index()
            
            all_experiments_avg_revenues = px.bar(
                avg_revenue_by_session,
                x='session',
                y='bid',
                title='Average Revenue Across All Experiments',
                labels={'session': 'Experiment Session', 'bid': 'Average Revenue'},
                color='session'
            ).to_html()
        else:
            all_experiments_avg_revenues = "<p>No data available for comparison</p>"
        
        return {
            'avg_bid_behavior_chart': avg_bid_behavior_chart,
            'individual_bid_behavior_charts': individual_bid_behavior_charts,
            'avg_revenue_chart': avg_revenue_chart,
            'avg_revenue_all_rounds': avg_revenue_all_rounds,
            'all_experiments_bid_behavior': all_experiments_bid_behavior,
            'all_experiments_revenue_trends': all_experiments_revenue_trends,
            'all_experiments_avg_revenues': all_experiments_avg_revenues
        }


page_sequence = [ResultsDashboard]
