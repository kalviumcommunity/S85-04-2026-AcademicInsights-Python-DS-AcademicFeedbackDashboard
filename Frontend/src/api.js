const API_BASE_URL = 'http://127.0.0.1:5000'

export async function predictSatisfaction(payload) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'Prediction request failed.')
  }

  return data
}
