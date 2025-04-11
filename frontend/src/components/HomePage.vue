<template>
  <div class="home">
    <h1>💩💩大作战</h1>
    <button @click="recordPoop(0)">0 💩</button>
    <button @click="recordPoop(1)">1 💩</button>
    <button @click="recordPoop(2)">2 💩</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePagetest',  // 修改为多词名称
  methods: {
    async recordPoop(count) {
      try {
        const response = await axios.post('http://localhost:5000/record_poop', {
          poop_count: count
        }, { withCredentials: true });
        alert(response.data.message);
      } catch (error) {
        console.error(error);
        alert('Error recording poop count!');
      }
    }
  }
}
</script>

<style scoped>
/* Add styles specific to the Home component */
</style>
