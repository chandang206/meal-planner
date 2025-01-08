 document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('ingredient-forms');
    const addButton = document.getElementById('add-ingredient');
    
    // Exit if the elements dont exist
    if (!container || !addButton) return;

    // New ingredient form
    addButton.addEventListener('click', function() {
        const formCount = container.children.length;
        const newForm = container.children[0].cloneNode(true);

        // Clear values
        newForm.querySelectorAll('input, select').forEach(input => {
            if (input.type === 'hidden' && input.name.includes('id')) {
                // Remove the id field value for new forms
                input.value = '';
            } else {
                input.value = '';
            }
            // Update form 
            input.name = input.name.replace(/-\d+-/, `-${formCount}-`);
            input.id = input.id.replace(/-\d+-/, `-${formCount}-`);
        });

        // Update labels
        newForm.querySelectorAll('label').forEach(label => {
            label.setAttribute('for', label.getAttribute('for').replace(/-\d+-/, `-${formCount}-`));
        });
        
        // Update form count
        const totalForms = document.querySelector('[name="ingredients-TOTAL_FORMS]');
        if (totalForms) {
            totalForms.value = formCount + 1;
        }
        container.appendChild(newForm);
    });

    // Remove ingredient form
    container.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-ingredient')) {
            if (container.children.length > 1) {
                e.target.closest('.ingredient-form').remove();
                const totalForms = document.querySelector('[name="ingredients-TOTAL_FORMS]');
                if (totalForms) {
                    totalForms.value = container.children.length;
                }

                // Update form indicies
                updateFormIndices();

            } else {
                alert('At least one ingredient is required!');
            }
        }
    });
    // Helper function to update form indices
    function updateFormIndices() {
        const forms = container.children;
        for (let i = 0; i < forms.length; i++) {
            const form = forms[i];
            form.querySelectorAll('input, select').forEach(input => {
                input.name = input.name.replace(/-\d+-/, `-${i}-`);
                input.id = input.id.replace(/-\d+-/, `-${i}-`);
            });
            form.querySelectorAll('label').forEach(label => {
                label.setAttribute('for', label.getAttribute('for').replace(/-\d+-/, `-${i}-`));
            });
        }
    }

});