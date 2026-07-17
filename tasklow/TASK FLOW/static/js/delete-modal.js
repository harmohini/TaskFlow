document.addEventListener('DOMContentLoaded', function() {
    // Set progress bar widths from data attributes
    document.querySelectorAll('[data-progress]').forEach(function(bar) {
        bar.style.width = bar.dataset.progress + '%';
    });

    // Set status badge colors based on data-status attribute
    document.querySelectorAll('.project-status-badge').forEach(function(badge) {
        const status = badge.dataset.status;
        if (status === 'Active') {
            badge.classList.add('bg-success');
        } else if (status === 'On Hold') {
            badge.classList.add('bg-warning', 'text-dark');
        } else if (status === 'Completed') {
            badge.classList.add('bg-primary');
        } else {
            badge.classList.add('bg-secondary');
        }
    });

    // Set member avatar colors based on data-role attribute
    document.querySelectorAll('.member-avatar-circle').forEach(function(circle) {
        const role = circle.dataset.role;
        if (role === 'Admin') {
            circle.classList.add('bg-primary');
        } else if (role === 'Viewer') {
            circle.classList.add('bg-secondary');
        } else {
            circle.classList.add('bg-info');
        }
    });

    // Set task priority badge colors
    document.querySelectorAll('.task-priority-badge').forEach(function(badge) {
        const priority = badge.dataset.priority;
        if (priority === 'High' || priority === 'Critical') {
            badge.classList.add('bg-danger');
        } else if (priority === 'Medium') {
            badge.classList.add('bg-warning', 'text-dark');
        } else {
            badge.classList.add('bg-success');
        }
    });

    // Set task status badge colors
    document.querySelectorAll('.task-status-badge').forEach(function(badge) {
        const status = badge.dataset.status;
        if (status === 'Completed') {
            badge.classList.add('bg-success');
        } else if (status === 'In Progress') {
            badge.classList.add('bg-info', 'text-dark');
        } else if (status === 'Review') {
            badge.classList.add('bg-warning', 'text-dark');
        } else {
            badge.classList.add('bg-secondary');
        }
    });

    // Event delegation for delete buttons
    document.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.btn-delete');
        if (deleteBtn) {
            const url = deleteBtn.dataset.deleteUrl;
            const name = deleteBtn.dataset.deleteName;
            document.getElementById('deleteItemName').textContent = name;
            document.getElementById('deleteForm').action = url;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        }
    });
});
