<template>
  <div ref="formulaContainer" class="p"></div>
</template>

<script setup lang="ts">
import katex from "katex";
import "katex/dist/katex.min.css";

const props = defineProps<{
  formula: string | undefined;
  displayMode?: boolean;
}>();

const formulaContainer = ref<HTMLDivElement>();

const renderFormula = () => {
  if (formulaContainer.value && props.formula) {
    try {
      katex.render(props.formula, formulaContainer.value, {
        displayMode: props.displayMode ?? true,
        throwOnError: false,
      });
    } catch (error) {
      console.error("Errore rendering LaTeX:", error);
      if (formulaContainer.value) {
        formulaContainer.value.textContent = props.formula;
      }
    }
  }
};

// Esegui il rendering quando il componente è montato
onMounted(() => {
  renderFormula();
});

// E anche quando la formula cambia
watch(
  () => props.formula,
  () => {
    renderFormula();
  }
);
</script>
