<template>
  <router-link to="/cart" class="btn btn-light position-relative me-3">
    🛒
    <span v-if="cartCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
      {{ cartCount }}
    </span>
  </router-link>
</template>

<script setup>
import { cartCount } from '@/stores/cart'
</script>
