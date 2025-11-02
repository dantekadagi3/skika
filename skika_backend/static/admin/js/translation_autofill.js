// Auto-fill Swahili translations when English options are selected
(function($) {
    'use strict';
    
    // Translation mappings (matching the Python TRANSLATION_MAPPINGS)
    const translations = {
        category: {
            'education': 'elimu',
            'infrastructure': 'miundombinu', 
            'health': 'afya',
            'water': 'maji',
            'environment': 'mazingira',
            'security': 'usalama',
            'other': 'mengine'
        },
        project_status: {
            'planned': 'imepangwa',
            'ongoing': 'inaendelea', 
            'completed': 'imekamilika',
            'stalled': 'imekwama'
        },
        report_status: {
            'received': 'imepokelewa',
            'under_review': 'chini_ya_ukaguzi',
            'action_taken': 'hatua_imechukuliwa',
            'resolved': 'imetatuliwa',
            'closed': 'imefungwa'
        },
        priority: {
            'low': 'chini',
            'medium': 'kati', 
            'high': 'juu'
        }
    };

    function autoFillSwahili(englishField, swahiliField, translationType) {
        const englishSelect = $('#' + englishField);
        const swahiliSelect = $('#' + swahiliField);
        
        if (englishSelect.length && swahiliSelect.length) {
            englishSelect.on('change', function() {
                const englishValue = $(this).val();
                const swahiliValue = translations[translationType][englishValue];
                
                if (swahiliValue) {
                    // Find and select the corresponding Swahili option
                    swahiliSelect.find('option').each(function() {
                        if ($(this).val() === swahiliValue) {
                            swahiliSelect.val(swahiliValue);
                            // Highlight the auto-filled field temporarily
                            swahiliSelect.addClass('auto-filled');
                            setTimeout(() => swahiliSelect.removeClass('auto-filled'), 2000);
                            return false;
                        }
                    });
                }
            });
        }
    }

    $(document).ready(function() {
        // Add CSS for auto-filled highlighting
        $('<style>')
            .prop('type', 'text/css')
            .html(`
                .auto-filled {
                    background-color: #e8f5e8 !important;
                    border: 2px solid #4caf50 !important;
                    transition: all 0.3s ease;
                }
                .translation-help {
                    background-color: #f0f8ff;
                    border: 1px solid #b0d4f1;
                    padding: 10px;
                    border-radius: 4px;
                    margin-bottom: 10px;
                }
            `)
            .appendTo('head');

        // Auto-fill for Project model
        autoFillSwahili('id_category_en', 'id_category_sw', 'category');
        autoFillSwahili('id_status_en', 'id_status_sw', 'project_status');

        // Auto-fill for Report model  
        autoFillSwahili('id_category_en', 'id_category_sw', 'category');
        autoFillSwahili('id_status_en', 'id_status_sw', 'report_status');
        autoFillSwahili('id_priority_level_en', 'id_priority_level_sw', 'priority');

        // Add help text
        $('fieldset:contains("Auto-fill Swahili")').each(function() {
            $(this).prepend(`
                <div class="translation-help">
                    <strong>🔄 Auto-Translation:</strong> 
                    When you select an English option, the corresponding Swahili field will be automatically filled. 
                    You can still manually override the Swahili selection if needed.
                </div>
            `);
        });

        // Show current translations in help text
        $('.field-category_en, .field-status_en, .field-priority_level_en').each(function() {
            const field = $(this);
            const select = field.find('select');
            const fieldName = select.attr('id');
            
            if (fieldName) {
                let translationType = '';
                if (fieldName.includes('category')) translationType = 'category';
                else if (fieldName.includes('status') && fieldName.includes('project')) translationType = 'project_status';
                else if (fieldName.includes('status')) translationType = 'report_status';
                else if (fieldName.includes('priority')) translationType = 'priority';
                
                if (translationType) {
                    select.on('focus', function() {
                        const currentValue = $(this).val();
                        const swahiliTranslation = translations[translationType][currentValue];
                        if (swahiliTranslation) {
                            $(this).attr('title', `Swahili: ${swahiliTranslation}`);
                        }
                    });
                }
            }
        });
    });

})(django.jQuery);