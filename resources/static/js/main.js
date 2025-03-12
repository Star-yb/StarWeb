// 添加页面加载动画效果
document.addEventListener('DOMContentLoaded', () => {
    const features = document.querySelectorAll('.feature-item');
    
    // 依次显示特性卡片
    features.forEach((feature, index) => {
        setTimeout(() => {
            feature.style.opacity = '1';
            feature.style.transform = 'translateY(0)';
        }, 200 * index);
    });
});
