<template>
  <div>
    <UCard
      class="mx-auto card my-10 p-10 sm:w-2xl lg:w-3xl xl:w-4xl"
      variant="soft"
    >
      <template #header>
        <div class="flex flex-col gap-2">
          <h1 class="h1">Calcolatore di Funzioni Inverse</h1>
          <p class="p">
            Inserisci una funzione e visualizza la sua funzione inversa con il
            grafico
          </p>
        </div>
      </template>
      <div>
        <UFormField label="Inserisci qui la funzione" :ui="{ label: 'subp' }">
          <UInput v-model="funzione" size="xl" class="w-full" />
          <UButton @click="getFunzioneInversa" class="my-2">Calcola</UButton>
        </UFormField>
      </div>
    </UCard>
    <div class="mx-8 grid grid-cols-1 lg:grid-cols-3 gap-4" v-if="fetchedData">
      <!-- Colonna sinistra con le card impilate -->
      <div class="flex flex-col gap-4">
        <UCard class="card p-6" variant="soft">
          <div class="flex flex-col gap-10">
            <div class="flex flex-col gap-2">
              <h2 class="h2 text-center">Funzione di Partenza</h2>
              <p class="subp text-center">Ecco la tua funzione di partenza</p>
              <LatexFormula
                :formula="fetchedData.funzione_di_partenza"
                :display-mode="true"
              />
            </div>
            <div class="flex flex-col gap-2">
              <h2 class="h2 text-center">Funzione Inversa</h2>
              <p class="subp text-center">Ecco la tua funzione inversa</p>
              <LatexFormula
                :formula="fetchedData.funzione_inversa"
                :display-mode="true"
              />
            </div>
          </div>
        </UCard>

        <!-- Card Studio della Funzione -->
        <UCard class="card p-6" variant="soft">
          <template #header>
            <div class="flex flex-col gap-2">
              <h2 class="h2">Studio della Funzione</h2>
              <p class="subp">Ecco qui lo studio della tua funzione.</p>
            </div>
          </template>

          <div class="flex flex-col gap-6">
            <!-- Nome -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Nome Funzione</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.nome_funzione }}
              </p>
            </div>

            <!-- Dominio -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Dominio</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.dominio }}
              </p>
            </div>

            <!-- Codominio -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Codominio</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.codominio }}
              </p>
            </div>

            <!-- Iniettività -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Iniettività</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.iniettivita }}
              </p>
            </div>

            <!-- Suriettività -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Suriettività</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.suriettivita }}
              </p>
            </div>

            <!-- Biettività -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Biettività</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.biettivita }}
              </p>
            </div>

            <!-- Monotonia -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Monotonia</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.monotonia }}
              </p>
            </div>

            <!-- Limiti -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Limiti</h3>
              <div class="text-sm space-y-1">
                <p>
                  <span class="font-medium">Per x → -∞:</span>
                  {{ fetchedData.studio_della_funzione.limiti.x_meno_infinito }}
                </p>
                <p>
                  <span class="font-medium">Per x → +∞:</span>
                  {{ fetchedData.studio_della_funzione.limiti.x_piu_infinito }}
                </p>
              </div>
            </div>

            <!-- Asintoti -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Asintoti</h3>
              <div class="text-sm space-y-1">
                <p
                  v-if="
                    fetchedData.studio_della_funzione.asintoti.verticali
                      .length === 0
                  "
                >
                  <span class="font-medium">Verticali:</span> Nessuno
                </p>
                <p
                  v-if="
                    fetchedData.studio_della_funzione.asintoti.orizzontali
                      .length === 0
                  "
                >
                  <span class="font-medium">Orizzontali:</span> Nessuno
                </p>
                <p
                  v-if="
                    fetchedData.studio_della_funzione.asintoti.obliqui
                      .length === 0
                  "
                >
                  <span class="font-medium">Obliqui:</span> Nessuno
                </p>
              </div>
            </div>

            <!-- Punti Notevoli -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Punti Notevoli</h3>
              <div class="text-sm space-y-1">
                <p
                  v-if="
                    fetchedData.studio_della_funzione.punti_notevoli
                      .intersezione_assi.x !== null
                  "
                >
                  <span class="font-medium">Intersezione asse x:</span>
                  ({{
                    fetchedData.studio_della_funzione.punti_notevoli
                      .intersezione_assi.x
                  }}, 0)
                </p>
                <p
                  v-if="
                    fetchedData.studio_della_funzione.punti_notevoli
                      .intersezione_assi.y !== null
                  "
                >
                  <span class="font-medium">Intersezione asse y:</span>
                  (0,
                  {{
                    fetchedData.studio_della_funzione.punti_notevoli
                      .intersezione_assi.y
                  }})
                </p>
              </div>
            </div>

            <!-- Descrizione Grafico -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Grafico Qualitativo</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.grafico_qualitativo }}
              </p>
            </div>

            <!-- Spiegazione Completa -->
            <div class="flex flex-col gap-2">
              <h3 class="font-semibold">Spiegazione Completa</h3>
              <p class="text-sm">
                {{ fetchedData.studio_della_funzione.spiegazione_completa }}
              </p>
            </div>
          </div>
        </UCard>
      </div>

      <!-- Grafico Completo -->
      <UCard class="card p-6 lg:col-span-2 h-fit" variant="soft">
        <template #header>
          <h2 class="h2">Grafico Completo</h2>
          <p class="subp">Ecco il grafico della tua funzione</p>
        </template>
        <XYChart
          :x-data="fetchedData.punti_x"
          :y-data="fetchedData.punti_y"
          class="w-full h-full"
        />
      </UCard>
    </div>
  </div>
</template>

<script lang="ts" setup>
interface StudioDellaFunzione {
  nome_funzione: string;
  dominio: string;
  codominio: string;
  iniettivita: string;
  suriettivita: string;
  biettivita: string;
  monotonia: string;
  limiti: {
    x_meno_infinito: string;
    x_piu_infinito: string;
    limiti_notevoli: [];
  };
  asintoti: {
    verticali: [];
    orizzontali: [];
    obliqui: [];
  };
  punti_notevoli: {
    intersezione_assi: {
      x: number | null;
      y: number | null;
    };
  };
  grafico_qualitativo: string;
  spiegazione_completa: string;
}

interface FunctionResult {
  funzione_di_partenza: string;
  funzione_inversa: string;
  punti_x: number[];
  punti_y: (number | null)[];
  studio_della_funzione: StudioDellaFunzione;
}

const funzione = ref<string>("");
const errore = ref<string>("");
const toast = useToast();
const fetchedData = ref<FunctionResult | null>(null);

const getFunzioneInversa = async () => {
  errore.value = "";
  fetchedData.value = null;
  const { data: risultato, error } = await useFetch<FunctionResult>(
    "http://127.0.0.1:8000/calcolo-analisi",
    {
      method: "POST",
      body: {
        function: funzione.value,
      },
    }
  );

  if (error.value) {
    errore.value = error.value.data?.detail || "Errore durante il calcolo";
    toast.add({
      title: "Errore",
      description: errore.value,
      color: "error",
      icon: "i-heroicons-exclamation-triangle",
    });
  } else if (risultato.value) {
    toast.add({
      title: "Successo",
      description: "Funzione inversa calcolata con successo",
      color: "success",
      icon: "i-heroicons-check-circle",
    });
    fetchedData.value = risultato.value;
  }
};
</script>
