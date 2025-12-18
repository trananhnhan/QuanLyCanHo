document.addEventListener('DOMContentLoaded', function() {
    const filterSelect = document.getElementById('filter-select');

    // Ánh xạ value của select box với ID của wrapper chứa input tương ứng
    const mapInput = {
        'ten': 'wrapper-ten',
        'phongngu': 'wrapper-phongngu',
        'songuoi': 'wrapper-songuoi'
    };

    filterSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        const targetId = mapInput[selectedValue];

        if (targetId) {
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                // 1. Hiện input đó lên (xóa class hidden)
                targetElement.classList.remove('hidden');

                // 2. Nếu là input group (giá) thì thêm d-flex, còn lại thêm d-block
                if (selectedValue === 'gia') {
                    targetElement.classList.add('d-flex');
                } else {
                    targetElement.classList.add('d-block');
                }

                // 3. Focus vào ô input để nhập luôn cho tiện
                const inputInside = targetElement.querySelector('input');
                if (inputInside) inputInside.focus();
            }
        }

        // 4. Quan trọng: Reset select box về mặc định để người dùng chọn tiếp cái khác
        this.value = 'none';
    });
});