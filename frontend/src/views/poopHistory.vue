<template>
    <div class="container">
        <div class="navbar">
            <NavBar />
        </div>
        <div class="header">
            <h1>Poop History</h1>
        </div>
        <div class="content">
            <poopHistory />
        </div>
    </div>    
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import poopHistory from "@/components/PoopHistorycomponent.vue";

export default {
    name: 'poopHistoryPage',
    components: {
        NavBar,
        poopHistory
    },
}
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    min-height: 100vh;
    background-color: #f5f5f5; /* 背景颜色 */
    font-family: Arial, sans-serif;
}

.navbar {
    width: 100%;
    height: 60px; /* 设置导航栏高度 */
    background-color: #2c3e50; /* 导航栏背景颜色 */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.header {
    margin: 20px 0;
    text-align: center;
}

.header h1 {
    font-size: 2rem;
    color: #34495e; /* 标题颜色 */
}

.content {
    width: 90%;
    max-width: 1200px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
    padding: 20px;
    margin-bottom: 20px;
}

.content h2 {
    font-size: 1.5rem;
    color: #2c3e50;
}

.content p {
    font-size: 1rem;
    color: #7f8c8d;
}
</style>