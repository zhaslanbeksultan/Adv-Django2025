<template>
  <v-container>
    <v-card>
      <v-card-title>Admin Panel</v-card-title>
      <v-btn color="red" @click="logout" class="ma-2">Logout</v-btn>
      <v-table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.description }}</td>
            <td>
              <v-btn color="red" @click="deleteItem(item.id)">Delete</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { getItems, deleteItem } from '../api';

export default {
  data() {
    return { items: [] };
  },
  computed: {
    ...mapState(['token']),
  },
  async created() {
    this.items = await getItems(this.token);
  },
  methods: {
    ...mapActions(['logout']),
    async deleteItem(id) {
      await deleteItem(id, this.token);
      this.items = this.items.filter(item => item.id !== id);
    },
  },
};
</script>