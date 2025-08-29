from otree.api import *
from .models import *
from .utils import get_all_auction_data, prepare_chart_data

class ResultsDashboard(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Get all auction data
        session = player.session
        all_data = get_all_auction_data(session)
        chart_data = prepare_chart_data(all_data)
        
        # Prepare data for the specific charts requested
        valuation_intervals = sorted(chart_data['valuation_distribution'].keys())
        valuation_counts = [chart_data['valuation_distribution'][interval] for interval in valuation_intervals]
        
        # Gender comparison data
        genders = list(chart_data['valuation_distribution_by_gender'].keys())
        gender_valuation_data = {}
        for gender in genders:
            gender_valuation_data[gender] = [chart_data['valuation_distribution_by_gender'][gender].get(interval, 0) for interval in valuation_intervals]
        
        # Average bid by valuation
        bid_intervals = sorted(chart_data['avg_bid_by_valuation'].keys())
        avg_bids = [chart_data['avg_bid_by_valuation'][interval] for interval in bid_intervals]
        
        # Demographic comparisons
        avg_bid_gender_labels = list(chart_data['avg_bid_by_gender'].keys())
        avg_bid_gender_values = [chart_data['avg_bid_by_gender'][gender] for gender in avg_bid_gender_labels]
        
        # Age groups
        age_groups = {
            '18-24': [], '25-34': [], '35-44': [], '45-54': [], '55+': []
        }
        for age, bids in chart_data['avg_bid_by_age'].items():
            if 18 <= age <= 24:
                age_groups['18-24'].append(bids)
            elif 25 <= age <= 34:
                age_groups['25-34'].append(bids)
            elif 35 <= age <= 44:
                age_groups['35-44'].append(bids)
            elif 45 <= age <= 54:
                age_groups['45-54'].append(bids)
            elif age >= 55:
                age_groups['55+'].append(bids)
        
        avg_bid_age_labels = list(age_groups.keys())
        avg_bid_age_values = [sum(bids)/len(bids) if bids else 0 for bids in age_groups.values()]
        
        # Race groups
        avg_bid_race_labels = list(chart_data['avg_bid_by_race'].keys())
        avg_bid_race_values = [chart_data['avg_bid_by_race'][race] for race in avg_bid_race_labels]
        
        return {
            # Chart 1: Valuation distribution
            'valuation_intervals': json.dumps([f"{int(interval)}-{int(interval)+19}" for interval in valuation_intervals]),
            'valuation_counts': json.dumps(valuation_counts),
            
            # Chart 2: Valuation distribution by gender
            'genders': json.dumps(genders),
            'gender_valuation_data': json.dumps([gender_valuation_data[gender] for gender in genders]),
            
            # Chart 3: Only women
            'women_valuation_counts': json.dumps([chart_data['valuation_distribution_women'].get(interval, 0) for interval in valuation_intervals]),
            
            # Chart 4: Only men  
            'men_valuation_counts': json.dumps([chart_data['valuation_distribution_men'].get(interval, 0) for interval in valuation_intervals]),
            
            # Chart 5: Average bid by gender
            'avg_bid_gender_labels': json.dumps(avg_bid_gender_labels),
            'avg_bid_gender_values': json.dumps(avg_bid_gender_values),
            
            # Chart 6: Average bid by age and race
            'avg_bid_age_labels': json.dumps(avg_bid_age_labels),
            'avg_bid_age_values': json.dumps(avg_bid_age_values),
            'avg_bid_race_labels': json.dumps(avg_bid_race_labels),
            'avg_bid_race_values': json.dumps(avg_bid_race_values),
            
            # Additional data for the specific player with valuation 50
            'player_valuation_50_data': [d for d in all_data if d['valuation'] == 50 and d.get('participant_code') == player.participant.code],
            'avg_bid_valuation_50': sum([d['bid'] for d in all_data if d['valuation'] == 50]) / len([d for d in all_data if d['valuation'] == 50]) if [d for d in all_data if d['valuation'] == 50] else 0,
            
            # Raw data for custom visualizations
            'chart_data': chart_data,
            'total_rounds': len(all_data),
            'total_participants': len(set([d.get('participant_code', '') for d in all_data]))
        }

page_sequence = [ResultsDashboard]
