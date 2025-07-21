import React, { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/authStore'
import { useThemeStore } from '@/stores/themeStore'

interface StockData {
  id: number
  symbol: string
  price: number
  volume: number
  date: string
}

export const Dashboard: React.FC = () => {
  const user = useAuthStore((state) => state.user)
  const effectiveTheme = useThemeStore((state) => state.effectiveTheme)
  const [stockData, setStockData] = useState<StockData[]>([])
  const [selectedSymbol, setSelectedSymbol] = useState<string>('')
  const [availableSymbols, setAvailableSymbols] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  
  // Chart theme based on mode
  const chartTheme = React.useMemo(() => ({
    grid: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
    axis: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)',
    tick: effectiveTheme === 'dark' ? 'rgba(255, 255, 255, 0.6)' : 'rgba(0, 0, 0, 0.6)',
    colors: [
      '#0070f3',  // Vercel blue
      '#7928ca',  // Purple
      '#ff0080',  // Pink
      '#ff4458',  // Red
      '#f5a623',  // Orange
      '#50e3c2',  // Teal
      '#b8e986'   // Green
    ]
  }), [effectiveTheme])

  const fetchStockData = async () => {
    setLoading(true)
    try {
      let url = '/api/v1/example/stocks'
      if (selectedSymbol) {
        url += `?symbol=${selectedSymbol}`
      }
      
      // Use fetch with credentials for custom API endpoints
      // The AllauthClient handles auth for allauth endpoints only
      const response = await fetch(url, {
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        }
      })
      if (!response.ok) {
        throw new Error('Failed to fetch stock data')
      }
      
      const data = await response.json()
      setStockData(data)
      
      // Only update available symbols if we're fetching all stocks
      // This prevents the dropdown from losing options when filtering
      if (!selectedSymbol) {
        const symbols = [...new Set(data.map((stock: StockData) => stock.symbol))].sort() as string[]
        setAvailableSymbols(symbols)
      }
    } catch (error) {
      console.error('Error fetching stock data:', error)
    } finally {
      setLoading(false)
    }
  }

  // Fetch all available symbols on mount
  useEffect(() => {
    const fetchAllSymbols = async () => {
      try {
        const response = await fetch('/api/v1/example/stocks', {
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
          }
        })
        if (response.ok) {
          const data = await response.json()
          const symbols = [...new Set(data.map((stock: StockData) => stock.symbol))].sort() as string[]
          setAvailableSymbols(symbols)
        }
      } catch (error) {
        console.error('Error fetching all symbols:', error)
      }
    }
    
    fetchAllSymbols()
  }, [])

  useEffect(() => {
    fetchStockData()
  }, [selectedSymbol])

  // Process data for charts
  const processedData = React.useMemo(() => {
    const groupedByDate: { [key: string]: any } = {}
    
    stockData.forEach(stock => {
      if (!groupedByDate[stock.date]) {
        groupedByDate[stock.date] = { date: stock.date }
      }
      groupedByDate[stock.date][`${stock.symbol}_price`] = stock.price
      groupedByDate[stock.date][`${stock.symbol}_volume`] = stock.volume
    })
    
    return Object.values(groupedByDate).sort((a, b) => 
      new Date(a.date).getTime() - new Date(b.date).getTime()
    )
  }, [stockData])

  const symbolsToDisplay = selectedSymbol ? [selectedSymbol] : availableSymbols

  return (
    <div className="w-full p-6 bg-background">
      <h2 className="text-3xl font-bold mb-4 text-foreground">Dashboard</h2>
      
      <div className="bg-card rounded-lg border border-border p-6 mb-6">
        <h3 className="text-xl font-semibold mb-2 text-foreground">Welcome, {user?.username || 'User'}!</h3>
        <p className="text-muted-foreground">This is your private dashboard. You can only see this page when logged in.</p>
      </div>

      <div className="bg-card rounded-lg border border-border p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-foreground">Stock Data</h2>
          <Button
            onClick={fetchStockData}
            disabled={loading}
            className="flex items-center gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        <div className="mb-6">
          <select
            value={selectedSymbol}
            onChange={(e) => setSelectedSymbol(e.target.value)}
            className="w-full max-w-xs px-3 py-2 bg-background border border-input rounded-md text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">All Stocks</option>
            {availableSymbols.map(symbol => (
              <option key={symbol} value={symbol}>{symbol}</option>
            ))}
          </select>
        </div>

        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">Stock Prices Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={processedData}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                <XAxis 
                  dataKey="date" 
                  stroke={chartTheme.axis}
                  tick={{ fill: chartTheme.tick }}
                  axisLine={{ stroke: chartTheme.axis }}
                />
                <YAxis 
                  stroke={chartTheme.axis}
                  tick={{ fill: chartTheme.tick }}
                  axisLine={{ stroke: chartTheme.axis }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--background))', 
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)'
                  }}
                  labelStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend 
                  wrapperStyle={{ paddingTop: '20px' }}
                  iconType="line"
                />
                {symbolsToDisplay.map((symbol, index) => (
                  <Line
                    key={symbol}
                    type="monotone"
                    dataKey={`${symbol}_price`}
                    name={symbol}
                    stroke={chartTheme.colors[index % chartTheme.colors.length]}
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 4 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">Trading Volume Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={processedData} margin={{ left: 20, right: 5, top: 5, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartTheme.grid} vertical={false} />
                <XAxis 
                  dataKey="date" 
                  stroke={chartTheme.axis}
                  tick={{ fill: chartTheme.tick }}
                  axisLine={{ stroke: chartTheme.axis }}
                />
                <YAxis 
                  stroke={chartTheme.axis}
                  tick={{ fill: chartTheme.tick }}
                  axisLine={{ stroke: chartTheme.axis }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'hsl(var(--background))', 
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)'
                  }}
                  labelStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend 
                  wrapperStyle={{ paddingTop: '20px' }}
                />
                {symbolsToDisplay.map((symbol, index) => (
                  <Bar
                    key={symbol}
                    dataKey={`${symbol}_volume`}
                    name={symbol}
                    fill={chartTheme.colors[index % chartTheme.colors.length]}
                    opacity={0.8}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}