const { BetaAnalyticsDataClient } = require('@google-analytics/data');

// Coloque aqui o ID da propriedade do Google Analytics do seu cliente
// Para achar: Google Analytics > Administrador > Configurações da propriedade > ID da propriedade (são apenas números)
const propertyId = '534388123';

// Inicializa o cliente do Google Analytics usando o arquivo JSON que você baixou
const analyticsDataClient = new BetaAnalyticsDataClient({
  keyFilename: './google-credentials.json',
});

async function runReport() {

  console.log(`Buscando dados da propriedade ${propertyId}...`);

  try {
    const [response] = await analyticsDataClient.runReport({
      property: `properties/${propertyId}`,
      dateRanges: [
        {
          startDate: '30daysAgo',
          endDate: 'today',
        },
      ],
      dimensions: [
        {
          name: 'city',
        },
      ],
      metrics: [
        {
          name: 'activeUsers',
        },
        {
          name: 'screenPageViews',
        }
      ],
    });

    console.log("✅ Conexão bem sucedida! Resultados dos últimos 30 dias:");
    console.log("--------------------------------------------------");

    if (response.rows.length === 0) {
      console.log("A API funcionou perfeitamente, mas essa propriedade ainda não tem dados de visitas registrados nos últimos 30 dias.");
    } else {
      response.rows.forEach(row => {
        console.log(
          `Cidade: ${row.dimensionValues[0].value} | ` +
          `Usuários Ativos: ${row.metricValues[0].value} | ` +
          `Visualizações de Página: ${row.metricValues[1].value}`
        );
      });
    }

  } catch (error) {
    console.error("❌ Ocorreu um erro ao buscar os dados:");
    console.error(error.message);
    if (error.message.includes('permission')) {
      console.log("\n⚠️ DICA: Parece um erro de permissão. Você tem certeza que adicionou o e-mail 'crm-analytics-fapa@...' como Leitor lá no painel do Google Analytics dessa propriedade?");
    }
  }
}

runReport();
