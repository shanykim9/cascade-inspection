// 전역 JavaScript 기능

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    // Feather icons 초기화
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // 폼 유효성 검사 초기화
    initFormValidation();
    
    // 반응형 메뉴 초기화
    initResponsiveMenu();
});

// 폼 유효성 검사
function initFormValidation() {
    // 회원가입 폼 검증
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            if (!validateRegisterForm()) {
                e.preventDefault();
                return false;
            }
        });
        
        // 실시간 패스워드 확인
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (password && confirmPassword) {
            confirmPassword.addEventListener('input', function() {
                if (password.value !== confirmPassword.value) {
                    confirmPassword.setCustomValidity('패스워드가 일치하지 않습니다.');
                } else {
                    confirmPassword.setCustomValidity('');
                }
            });
        }
        
        // 사번 숫자만 입력
        const employeeId = document.getElementById('employee_id');
        if (employeeId) {
            employeeId.addEventListener('input', function(e) {
                e.target.value = e.target.value.replace(/[^0-9]/g, '');
            });
        }
        
        // 전화번호 포맷팅
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/[^0-9]/g, '');
                let formattedValue = '';
                
                if (value.length > 0) {
                    if (value.length <= 3) {
                        formattedValue = value;
                    } else if (value.length <= 7) {
                        formattedValue = value.slice(0, 3) + '-' + value.slice(3);
                    } else {
                        formattedValue = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
                    }
                }
                
                e.target.value = formattedValue;
            });
        }
    }
}

// 회원가입 폼 유효성 검사
function validateRegisterForm() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const employeeId = document.getElementById('employee_id').value.trim();
    
    // 필수 입력 확인
    if (!username || !password || !confirmPassword || !name || !phone || !employeeId) {
        showAlert('모든 항목을 입력해주세요.', 'error');
        return false;
    }
    
    // 패스워드 길이 확인
    if (password.length < 6) {
        showAlert('패스워드는 최소 6자 이상이어야 합니다.', 'error');
        return false;
    }
    
    // 패스워드 확인
    if (password !== confirmPassword) {
        showAlert('패스워드가 일치하지 않습니다.', 'error');
        return false;
    }
    
    // 사번 숫자 확인
    if (!/^\d+$/.test(employeeId)) {
        showAlert('사번은 숫자만 입력 가능합니다.', 'error');
        return false;
    }
    
    // 전화번호 형식 확인
    if (!/^[0-9\-]+$/.test(phone)) {
        showAlert('전화번호 형식이 올바르지 않습니다.', 'error');
        return false;
    }
    
    return true;
}

// 반응형 메뉴 초기화
function initResponsiveMenu() {
    // 모바일 메뉴 토글 기능 (필요시 추가)
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// 알림 메시지 표시
function showAlert(message, type = 'info') {
    const flashMessages = document.getElementById('flash-messages');
    if (!flashMessages) return;
    
    const alertDiv = document.createElement('div');
    const colorClass = type === 'error' ? 'red' : type === 'success' ? 'green' : type === 'warning' ? 'yellow' : 'blue';
    const iconName = type === 'error' ? 'alert-circle' : type === 'success' ? 'check-circle' : type === 'warning' ? 'alert-triangle' : 'info';
    
    alertDiv.className = `alert alert-${type} bg-${colorClass}-100 border-l-4 border-${colorClass}-500 text-${colorClass}-700 p-4 mb-4 mx-4 mt-4 rounded shadow-lg`;
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i data-feather="${iconName}" class="w-5 h-5 mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-auto">
                <i data-feather="x" class="w-4 h-4"></i>
            </button>
        </div>
    `;
    
    flashMessages.appendChild(alertDiv);
    
    // Feather icons 다시 초기화
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // 5초 후 자동 제거
    setTimeout(() => {
        alertDiv.style.transition = 'opacity 0.5s ease-out';
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 500);
    }, 5000);
}

// API 호출 헬퍼 함수
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showAlert('서버와의 통신에 실패했습니다.', 'error');
        throw error;
    }
}

// 로딩 상태 표시
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="flex items-center justify-center"><i data-feather="loader" class="w-5 h-5 animate-spin mr-2"></i>로딩 중...</div>';
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}

// 로딩 상태 숨김
function hideLoading() {
    // 필요시 구현
}

// 날짜 포맷팅
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// 권한 확인
function hasPermission(userRole, requiredPermission) {
    const permissions = {
        'input': ['input'],
        'download': ['input', 'download'],
        'admin': ['input', 'download', 'admin']
    };
    
    return permissions[userRole]?.includes(requiredPermission) || false;
}

// 페이지 새로고침 없이 컨텐츠 업데이트
function updateContent(selector, content) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerHTML = content;
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}

// 모바일 환경 감지
function isMobile() {
    return window.innerWidth <= 768;
}

// 윈도우 리사이즈 이벤트
window.addEventListener('resize', function() {
    // 반응형 레이아웃 조정 (필요시 추가)
});

// 에러 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // 개발 환경에서만 에러 표시
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        showAlert('JavaScript 오류가 발생했습니다. 콘솔을 확인해주세요.', 'error');
    }
});

// 서비스 워커 등록 (PWA 기능, 필요시 활성화)
/*
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
*/
