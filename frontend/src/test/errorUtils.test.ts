import { describe, it, expect } from 'vitest'
import { toErrorMessage } from '../utils/errorUtils'

describe('toErrorMessage', () => {
  it('returns message from an Error', () => {
    expect(toErrorMessage(new Error('oops'))).toBe('oops')
  })

  it('converts a string to string', () => {
    expect(toErrorMessage('bad')).toBe('bad')
  })

  it('converts a number to string', () => {
    expect(toErrorMessage(500)).toBe('500')
  })

  it('converts null to string', () => {
    expect(toErrorMessage(null)).toBe('null')
  })
})
