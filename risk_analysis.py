"""
Risk Analysis Module for Mosquito Detection App
Calculates risk levels based on mosquito density per square meter
"""

def calculate_risk_level(density):
    """
    Calculate risk level based on mosquito density per square meter
    
    Args:
        density (float): Number of mosquitoes per square meter
        
    Returns:
        tuple: (risk_level, color, emoji, description)
    """
    if density < 0.5:
        return (
            "Low Risk", 
            "#28a745", 
            "🟢", 
            "Minimal disease transmission risk. Continue regular monitoring."
        )
    elif density < 2.0:
        return (
            "Medium Risk", 
            "#ffc107", 
            "🟡", 
            "Moderate risk. Consider implementing control measures."
        )
    else:
        return (
            "High Risk", 
            "#dc3545", 
            "🔴", 
            "High disease transmission risk! Immediate intervention recommended."
        )


def get_risk_metrics(mosquito_count, area_sqm):
    """
    Calculate comprehensive risk metrics
    
    Args:
        mosquito_count (int): Total number of mosquitoes detected
        area_sqm (float): Area in square meters
        
    Returns:
        dict: Dictionary containing all risk metrics
    """
    # Calculate density (mosquitoes per square meter)
    if area_sqm > 0:
        density = mosquito_count / area_sqm
    else:
        density = 0
    
    # Get risk level
    risk_level, color, emoji, description = calculate_risk_level(density)
    
    return {
        "mosquito_count": mosquito_count,
        "area_sqm": round(area_sqm, 4),
        "density": round(density, 2),
        "risk_level": risk_level,
        "color": color,
        "emoji": emoji,
        "description": description
    }
