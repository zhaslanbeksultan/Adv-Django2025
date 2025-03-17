<template>
  <v-container>
    <v-card>
      <v-card-title>Items</v-card-title>
      <v-list>
        <v-list-item v-for="item in items" :key="item.id">
          {{ item.name }} - {{ item.description }}
        </v-list-item>
      </v-list>
      <v-form @submit.prevent="addItem">
        <v-text-field v-model="newItem.name" label="Name" required></v-text-field>
        <v-text-field v-model="newItem.description" label="Description" required></v-text-field>
        <v-btn type="submit" color="primary">Add Item</v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import { getItems, createItem } from '../api';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      items: [],
      newItem: { name: '', description: '' },
    };
  },
  computed: {
    ...mapState(['token']),
  },
  async created() {
    this.items = await getItems(this.token);
  },
  methods: {
    async addItem() {
      const item = await createItem(this.newItem, this.token);
      this.items.push(item);
      this.newItem = { name: '', description: '' };
    },
  },
};
</script>