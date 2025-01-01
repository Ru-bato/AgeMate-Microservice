<<<<<<< HEAD
<template>
    <div class="home-view">
        <NavBar :username="username" :authority="authority" />
        <div class="content">
            <router-view /> <!-- 这里显示子页面 -->
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps,onMounted } from 'vue';
import { useRouter } from 'vue-router';
import NavBar from '@/components/NavBar.vue';

const router = useRouter();

const props = defineProps({
    username: {
        type: String,
        required: true,
    },
    authority: {
        type: Number,
        required: true,
    },
});

onMounted(() => {
    router.push({name:"HomePage",params:{username:props.username,authority:props.authority}})
})
</script>

<style scoped>
.home-view {
    display: flex;
}

.navbar {
    width: 250px;
    background-color: #2c3e50;
    color: white;
}

.content {
    margin-left: 250px;
    flex-grow: 1;
    padding: 20px;
}
</style>
=======
<template>
  <!-- <div class="home-view">
    <NavBar :username="username" :authority="authority" />
    <TopBar :username="username" :authority="authority" />
    <div class="content">
      <router-view />
    </div>
  </div> -->

  <el-container>
    <el-header>
      <NavBar :username="username" :authority="authority" />
    </el-header>
    <el-container>
      <el-aside>
        <TopBar :username="username" :authority="authority" />
      </el-aside>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import TopBar from '@/components/TopBar.vue'
import NavBar from '@/components/NavBar.vue'
import { defineProps } from 'vue'

const props = defineProps({
  username: {
    type: String,
    required: true,
  },
  authority: {
    type: Number,
    required: true,
  },
})

const username = props.username
const authority = props.authority
</script>

<style scoped>
.home-view {
  display: flex;
}

.content {

  min-height: 100vh;
}
</style>
>>>>>>> origin/bsh
