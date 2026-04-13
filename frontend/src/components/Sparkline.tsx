interface Props {
  data: number[]
  height?: number
  colour?: string
}

export function Sparkline({ data, height = 24, colour = '#3b82f6' }: Props) {
  if (data.length === 0) return <div style={{ height }} className="bg-slate-900 rounded" />

  const max = Math.max(...data, 1)
  const barWidth = 100 / data.length

  return (
    <svg viewBox={`0 0 100 ${height}`} className="w-full" style={{ height }} preserveAspectRatio="none">
      {data.map((v, i) => {
        const barHeight = (v / max) * height
        return (
          <rect
            key={i}
            x={i * barWidth + 0.5}
            y={height - barHeight}
            width={barWidth - 1}
            height={barHeight}
            fill={colour}
            opacity={i === data.length - 1 ? 1 : 0.4}
            rx={1}
          />
        )
      })}
    </svg>
  )
}
