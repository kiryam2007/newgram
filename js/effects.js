// Visual Effects

document.addEventListener('DOMContentLoaded', () => {
  // Add floating animation to feature icons
  const featureIcons = document.querySelectorAll('.feature-icon');
  featureIcons.forEach((icon, index) => {
    icon.style.animationDelay = `${index * 0.2}s`;
    icon.classList.add('floating');
  });

  // Add parallax effect on scroll
  const hero = document.querySelector('.hero');
  if (hero) {
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      const heroContent = hero.querySelector('.fade-in, h1');
      if (heroContent) {
        heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
      }
    });
  }

  // Add typing effect to hero text
  const heroH1 = document.querySelector('.hero h1');
  if (heroH1) {
    const text = heroH1.innerHTML;
    heroH1.style.opacity = '0';
    setTimeout(() => {
      heroH1.style.opacity = '1';
      heroH1.style.transition = 'opacity 0.5s';
    }, 300);
  }

  // Add hover effect to service features
  const serviceFeatures = document.querySelectorAll('.service-feature');
  serviceFeatures.forEach(feature => {
    feature.addEventListener('mouseenter', () => {
      feature.style.color = '#fff';
      feature.style.transform = 'translateX(5px)';
      feature.style.transition = 'all 0.3s';
    });
    feature.addEventListener('mouseleave', () => {
      feature.style.color = '#a0a0b0';
      feature.style.transform = 'translateX(0)';
    });
  });

  // Add glow effect to tech items on hover
  const techItems = document.querySelectorAll('.tech-item');
  techItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
      item.style.boxShadow = '0 0 20px rgba(108, 92, 231, 0.3)';
    });
    item.addEventListener('mouseleave', () => {
      item.style.boxShadow = 'none';
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Add animation to form inputs
  const formInputs = document.querySelectorAll('.form-group input, .form-group textarea');
  formInputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.parentElement.style.transform = 'translateY(-2px)';
      input.parentElement.style.transition = 'transform 0.3s';
    });
    input.addEventListener('blur', () => {
      input.parentElement.style.transform = 'translateY(0)';
    });
  });
});
