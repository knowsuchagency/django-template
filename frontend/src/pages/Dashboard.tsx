import React, { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAllauth } from '@knowsuchagency/allauth-react'

interface StockData {
  id: number
  symbol: string
  price: number
  volume: number
  date: string
}

export const Dashboard: React.FC = () => {
  const { user } = useAllauth()
  const [stockData, setStockData] = useState<StockData[]>([])
  const [selectedSymbol, setSelectedSymbol] = useState<string>('')
  const [availableSymbols, setAvailableSymbols] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

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
    <div className="w-full p-6">
      <h2 className="text-3xl font-bold mb-4">Dashboard</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-xl font-semibold mb-2">Welcome, {user?.username || 'User'}!</h3>
        <p className="text-gray-600">This is your private dashboard. You can only see this page when logged in.</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Stock Data</h2>
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
            className="w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Stocks</option>
            {availableSymbols.map(symbol => (
              <option key={symbol} value={symbol}>{symbol}</option>
            ))}
          </select>
        </div>

        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Stock Prices Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={processedData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                {symbolsToDisplay.map((symbol, index) => (
                  <Line
                    key={symbol}
                    type="monotone"
                    dataKey={`${symbol}_price`}
                    name={symbol}
                    stroke={`hsl(${index * 360 / symbolsToDisplay.length}, 70%, 50%)`}
                    strokeWidth={2}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Trading Volume Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={processedData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                {symbolsToDisplay.map((symbol, index) => (
                  <Bar
                    key={symbol}
                    dataKey={`${symbol}_volume`}
                    name={symbol}
                    fill={`hsl(${index * 360 / symbolsToDisplay.length}, 70%, 50%)`}
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