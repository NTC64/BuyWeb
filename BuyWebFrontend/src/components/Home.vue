<script setup>
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
    <div>
        <h1>Home</h1>
        <button @click="count++">Click me</button>
        <p>Count is {{ count }}</p>
    </div>
    <div>
        <h1>Home</h1>
        <button @click="count++">Click me</button>
        <p>Count is {{ count }}</p>
    </div>
    <div>
        <h1>Home</h1>
        <button @click="count++">Click me</button>
        <p>Count is {{ count }}</p>
    </div>
</template>