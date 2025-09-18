// Test script to verify frontend-backend communication
// Run this in browser console at localhost:3000

async function testAPIConnection() {
  try {
    console.log('🔄 Testing API connection...');
    
    // Test health endpoint
    const healthResponse = await fetch('http://localhost:8004/health');
    const healthData = await healthResponse.json();
    console.log('✅ Health check:', healthData);
    
    // Test quick world generation
    const worldResponse = await fetch('http://localhost:8004/generate_safe_world_quick', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: 'I feel happy today',
        include_media: false
      })
    });
    
    const worldData = await worldResponse.json();
    console.log('✅ World generation:', worldData);
    
    return { health: healthData, world: worldData };
  } catch (error) {
    console.error('❌ API test failed:', error);
    return null;
  }
}

// Run the test
testAPIConnection();
