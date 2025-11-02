"""
Translation utilities for Skika Backend
Provides helper functions for English-Swahili translations
"""

from core.models import TRANSLATION_MAPPINGS, get_swahili_translation


def translate_choice_field(english_value, field_type):
    """
    Get Swahili translation for a choice field value
    
    Args:
        english_value (str): The English choice value
        field_type (str): Type of field (category, project_status, report_status, priority)
        
    Returns:
        str: Swahili translation or original value if not found
    """
    return get_swahili_translation(field_type, english_value)


def get_all_translations():
    """Get all available translations"""
    return TRANSLATION_MAPPINGS


def get_choice_pairs(field_type):
    """
    Get English-Swahili choice pairs for a field type
    
    Args:
        field_type (str): Type of field
        
    Returns:
        list: List of (english_key, swahili_key) tuples
    """
    if field_type not in TRANSLATION_MAPPINGS:
        return []
    
    return [(en_key, sw_value) for en_key, sw_value in TRANSLATION_MAPPINGS[field_type].items()]


def validate_translation_consistency(english_value, swahili_value, field_type):
    """
    Check if English and Swahili values match the expected translation
    
    Args:
        english_value (str): English choice value
        swahili_value (str): Swahili choice value  
        field_type (str): Type of field
        
    Returns:
        bool: True if values are consistent, False otherwise
    """
    expected_swahili = get_swahili_translation(field_type, english_value)
    return swahili_value == expected_swahili


# Translation mappings for display purposes
DISPLAY_TRANSLATIONS = {
    'category': {
        'education': 'Elimu',
        'infrastructure': 'Miundombinu', 
        'health': 'Afya',
        'water': 'Maji',
        'environment': 'Mazingira',
        'security': 'Usalama',
        'other': 'Mengine'
    },
    'project_status': {
        'planned': 'Imepangwa',
        'ongoing': 'Inaendelea', 
        'completed': 'Imekamilika',
        'stalled': 'Imekwama'
    },
    'report_status': {
        'received': 'Imepokelewa',
        'under_review': 'Chini ya Ukaguzi',
        'action_taken': 'Hatua Imechukuliwa',
        'resolved': 'Imetatuliwa',
        'closed': 'Imefungwa'
    },
    'priority': {
        'low': 'Chini',
        'medium': 'Kati', 
        'high': 'Juu'
    }
}


def get_display_translation(field_type, english_value):
    """Get properly capitalized Swahili translation for display"""
    return DISPLAY_TRANSLATIONS.get(field_type, {}).get(english_value, english_value)