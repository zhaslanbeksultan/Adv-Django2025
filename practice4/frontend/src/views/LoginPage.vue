<template>
  <v-container>
    <v-card class="mx-auto pa-4" max-width="400">
      <v-card-title>Login</v-card-title>
      <v-form @submit.prevent="submitLogin">
        <v-text-field v-model="username" label="Username" required></v-text-field>
        <v-text-field v-model="password" type="password" label="Password" required></v-text-field>
        <v-btn type="submit" color="primary" block>Login</v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {username: '', password: ''};
  },
  methods: {
    ...mapActions(['login']),
    async submitLogin() {
      try {
        await this.login({username: this.username, password: this.password});
        this.$router.push('/admin');
      } catch (error) {
        console.error('Login failed:', error);
      }
    },
  },
};
</script>