"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"

interface Feedback {
  comment: string
  rating: number
}

interface SentimentResult {
  positive: number
  neutral: number
  negative: number
  score: number
}

export default function SentimentAnalyzer({ feedback }: { feedback: Feedback[] }) {
  const [sentiment, setSentiment] = useState<SentimentResult>({
    positive: 0,
    neutral: 0,
    negative: 0,
    score: 0,
  })

  useEffect(() => {
    if (feedback.length === 0) return

    // Simple sentiment analysis based on feedback
    let positiveCount = 0
    let neutralCount = 0
    let negativeCount = 0

    feedback.forEach((item) => {
      // Combine rating and comment for sentiment
      const comment = item.comment.toLowerCase()

      // Keywords analysis
      const positiveKeywords = [
        "good",
        "excellent",
        "great",
        "awesome",
        "wonderful",
        "satisfied",
        "happy",
        "thanks",
        "appreciate",
      ]
      const negativeKeywords = [
        "bad",
        "poor",
        "terrible",
        "awful",
        "worse",
        "dissatisfied",
        "angry",
        "disappointed",
        "hate",
      ]

      const hasPositive = positiveKeywords.some((keyword) => comment.includes(keyword))
      const hasNegative = negativeKeywords.some((keyword) => comment.includes(keyword))

      // Combine with rating
      if (item.rating >= 4) {
        positiveCount++
      } else if (item.rating === 3) {
        neutralCount++
      } else if (item.rating <= 2) {
        negativeCount++
      }

      // Override with keyword detection
      if (hasPositive && !hasNegative) {
        positiveCount++
      } else if (hasNegative && !hasPositive) {
        negativeCount++
      }
    })

    // Normalize counts
    const total = feedback.length
    const sentimentScore = ((positiveCount - negativeCount) / total) * 100

    setSentiment({
      positive: Math.round((positiveCount / total) * 100),
      neutral: Math.round((neutralCount / total) * 100),
      negative: Math.round((negativeCount / total) * 100),
      score: sentimentScore,
    })
  }, [feedback])

  const sentimentData = [
    { name: "Positive", value: sentiment.positive, color: "#10b981" },
    { name: "Neutral", value: sentiment.neutral, color: "#f59e0b" },
    { name: "Negative", value: sentiment.negative, color: "#ef4444" },
  ]

  const chartData = sentimentData.filter((item) => item.value > 0)

  const getSentimentLabel = () => {
    if (sentiment.score > 30) return "Highly Positive"
    if (sentiment.score > 10) return "Positive"
    if (sentiment.score > -10) return "Neutral"
    if (sentiment.score > -30) return "Negative"
    return "Highly Negative"
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Overall Sentiment
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{getSentimentLabel()}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">
              Score: {sentiment.score.toFixed(1)}
            </p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Positive
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">{sentiment.positive}%</div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Neutral
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{sentiment.neutral}%</div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Negative
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-600 dark:text-red-400">{sentiment.negative}%</div>
          </CardContent>
        </Card>
      </div>

      {/* Sentiment Distribution Chart */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Sentiment Distribution</CardTitle>
          <CardDescription>Breakdown of citizen feedback sentiment</CardDescription>
        </CardHeader>
        <CardContent>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value}%`} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-80 flex items-center justify-center text-foreground-muted dark:text-foreground-dark-muted">
              No sentiment data available
            </div>
          )}
        </CardContent>
      </Card>

      {/* Sentiment Trends */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Sentiment Insights</CardTitle>
          <CardDescription>Key findings from citizen feedback</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <span className="text-2xl">✅</span>
              <div>
                <p className="font-medium text-green-900 dark:text-green-100">
                  Positive Feedback: {sentiment.positive}%
                </p>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Citizens are generally satisfied with services
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="font-medium text-yellow-900 dark:text-yellow-100">
                  Neutral Feedback: {sentiment.neutral}%
                </p>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">
                  Some citizens have mixed views - opportunity for improvement
                </p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
              <span className="text-2xl">❌</span>
              <div>
                <p className="font-medium text-red-900 dark:text-red-100">Negative Feedback: {sentiment.negative}%</p>
                <p className="text-sm text-red-700 dark:text-red-300">
                  Priority areas requiring attention and follow-up
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
