<template>
  <div class="home-wrapper">
    <div class="container">
      <HeroBanner />
      <FeaturedProducts />
      <PromoSection />
      <AboutSection />
      <WhyChooseUs />
      <BlogTeaser />
      <NewsletterCTA />
    </div>
  </div>
</template>

<script setup>
import HeroBanner from '@/components/Home/HeroBanner.vue'
import FeaturedProducts from '@/components/Home/FeaturedProducts.vue'
import PromoSection from '@/components/Home/PromoSection.vue'
import AboutSection from '@/components/Home/AboutSection.vue'
import WhyChooseUs from '@/components/Home/WhyChooseUs.vue'
import BlogTeaser from '@/components/Home/BlogTeaser.vue'
import NewsletterCTA from '@/components/Home/NewsletterCTA.vue'
</script>

<style>
.home-wrapper {
  background-color: #f1f8f4; /* vert clair doux */
  min-height: 100vh;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
</style>
