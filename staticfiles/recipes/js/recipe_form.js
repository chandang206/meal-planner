 document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('ingredient-forms');
    const addButton = document.getElementById('add-ingredient');
    const totalForms = document.getElementById('id_ingredient-TOTAL_FORMS');

    // New ingredient form
    addButton.addEventListener('click', function() {
        const formCount = container.children.length;
        const newForm = container.children[0].cloneNode(true);

        // Clear values
        newForm.querySelectorAll('input').forEach(input => {
            input.value = '';
            // Update form 
            input.name = input.name.replace('-0-', `-${formCount}-`);
            input.id = input.id.replace('-0-', `-${formCount}-`);
        });
        
        // Update form count
        totalForms.value = formCount + 1;
        container.appendChild(newForm);
    });

    // Remove ingredient form
    container.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-ingredient')) {
            if (container.children.length > 1) {
                e.target.closest('.ingredient-form').remove();
                totalForms.value = container.children.length;
            } else {
                alert('At least one ingredient is required!');
            }
        }
    });
});